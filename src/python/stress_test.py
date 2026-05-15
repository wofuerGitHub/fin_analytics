#!/usr/bin/python3
from datetime import datetime
import numpy as np
import pandas as pd

from mylib import config
from mylib.writeLog import writeLog
from mylib import mysql_db

METHOD = "drawdown_3y"
LOG_TEXT = " rolling 3y drawdown of current-weight portfolio"

CONFIG = config.load_config('config.json')["analytics"]
log_id = CONFIG.get(METHOD, {}).get('log_id', 0)
writeLog(CONFIG['file']['log'], 'Start ' + LOG_TEXT, id=log_id)

mysql_db.set_configuration(**CONFIG["database"])
sql_engine = mysql_db.create_sql_engine(mysql_db.get_configuration())


def max_drawdown(series: pd.Series):
    """
    Returns:
      mdd (float, negative), peak_date, trough_date
    """
    s = series.dropna()
    if len(s) < 2:
        return np.nan, None, None
    running_max = s.cummax()
    dd = s / running_max - 1.0
    trough = dd.idxmin()
    peak = s.loc[:trough].idxmax() if trough is not None else None
    return float(dd.loc[trough]), peak, trough


def compute_rolling_3y_portfolio_mdd(
    prices: pd.DataFrame,
    weights: pd.Series,
    horizon_years: int = 3,
    start_freq: str = "MS",   # month start
    calendar: str = "B",      # business days
    require_all_assets: bool = True,
):
    """
    prices:  DataFrame indexed by date, columns = symbols, values = close prices
    weights: Series indexed by symbol, sum ~ 1
    """
    # align + clean
    prices = prices.sort_index()
    # unify calendar and fill gaps (EU/US holiday mismatches etc.)
    prices = prices.asfreq(calendar).ffill()

    # use latest date where all assets have prices (after ffill it should be last index,
    # but keep it robust if some series start later)
    if require_all_assets:
        last_common = prices.dropna().index.max()
    else:
        last_common = prices.index.max()

    last_common = pd.to_datetime(last_common)
    if pd.isna(last_common):
        raise ValueError("No common price date found (all NaN).")

    latest_allowed_start = last_common - pd.DateOffset(years=horizon_years)

    # monthly starts from first available date to last allowed start
    month_starts = pd.date_range(
        start=prices.index.min().normalize(),
        end=latest_allowed_start.normalize(),
        freq=start_freq
    )

    results = []
    for ms in month_starts:
        # map to next available business day in index
        i0 = prices.index.searchsorted(ms)
        if i0 >= len(prices.index):
            continue
        t0 = prices.index[i0]
        t1 = t0 + pd.DateOffset(years=horizon_years)
        if t1 > last_common:
            continue

        window = prices.loc[t0:t1]
        if len(window) < 2:
            continue

        # require weights assets to be present
        cols = [c for c in weights.index if c in window.columns]
        w = weights.loc[cols].copy()

        # if any asset missing at t0 (still NaN), skip or renormalize
        p0 = window.iloc[0][cols]
        if require_all_assets and p0.isna().any():
            continue
        if (not require_all_assets) and p0.isna().any():
            # drop missing and renormalize
            ok = ~p0.isna()
            cols = list(p0.index[ok])
            w = w.loc[cols]
            w = w / w.sum()
            window = window[cols]
            p0 = window.iloc[0]

        # portfolio path with fixed weights:
        # V(t) = sum_i w_i * (P_i(t)/P_i(t0))
        rel = window[cols].div(p0, axis=1)
        port = rel.mul(w, axis=1).sum(axis=1)

        mdd, peak, trough = max_drawdown(port)
        results.append({
            "start": t0,
            "end": window.index[-1],
            "max_drawdown": mdd,
            "peak": peak,
            "trough": trough,
        })

    out = pd.DataFrame(results).sort_values("max_drawdown")  # most negative first
    return out


# ------------------------
# 1) load portfolio + reference (same pattern as your optimizer)
# ------------------------
print("load portfolio")
connection_to_source = sql_engine.connect()
source = mysql_db.get_metatable(sql_engine, CONFIG["optimization_2"]["table_source_portfolio"])
my_portfolio = mysql_db.get_mysql_data(connection_to_source, source,
                                       columns=CONFIG["optimization_2"]["columns_source_portfolio"])
connection_to_source.close()

connection_to_source = sql_engine.connect()
source = mysql_db.get_metatable(sql_engine, CONFIG["optimization_2"]["table_source_reference"])
reference = mysql_db.get_mysql_data(connection_to_source, source,
                                    columns=CONFIG["optimization_2"]["columns_source_reference"])
connection_to_source.close()

my_portfolio = pd.merge(reference, my_portfolio[['symbol', 'all']], how="left", on=['symbol'])
my_portfolio['all'] = my_portfolio['all'].fillna(0)
my_portfolio = my_portfolio[my_portfolio['all'] != 0].copy()

symbols = my_portfolio['symbol'].tolist()

# ------------------------
# 2) load a LONG enough history of closes for rolling 3y windows
# ------------------------
print("load timeseries (long history)")
years_back = 20           # how far back you want MONTHLY start points to go
horizon_years = 3

first_date = (datetime.now()
              - pd.DateOffset(years=years_back + horizon_years)
             ).strftime("%Y-%m-%d")

prices = pd.DataFrame()

for _, row in my_portfolio.iterrows():
    sym = row['symbol']
    qty = float(row['all'])

    connection_to_source = sql_engine.connect()
    source = mysql_db.get_metatable(sql_engine, CONFIG["optimization_2"]["table_source_ts"])
    ts = mysql_db.get_mysql_data(connection_to_source, source,
                                 columns=CONFIG["optimization_2"]["columns_source_ts"],
                                 filter_symbol=sym,
                                 filter_date=first_date,
                                 order_desc=False)
    connection_to_source.close()

    ts.date = pd.to_datetime(ts.date)
    ts = ts.set_index('date').sort_index()

    # use CLOSE prices (swap to adjclose/total_return if you have it)
    prices[sym] = ts['close'].astype(float)

# align calendar + forward fill (important for mixed exchanges)
prices = prices.sort_index().asfreq("B").ffill()

# ------------------------
# 3) compute TODAY (latest common) VALUE weights from qty * price
# ------------------------
# last date (use latest row, but if NaN: replace with the FIRST available value of that symbol)
last_common = prices.index.max()

last_prices = prices.loc[last_common, symbols].copy()

# first non-NaN value per symbol (earliest available observation)
first_prices = prices[symbols].apply(lambda s: s.dropna().iloc[0] if s.notna().any() else np.nan)

# fill NaNs in last_prices with that first available value
last_prices = last_prices.fillna(first_prices)

values = last_prices.values * my_portfolio.set_index('symbol').loc[symbols, 'all'].astype(float).values
weights = pd.Series(values / np.sum(values), index=symbols, name="w")

print(f"latest common date used for weights: {last_common.date()}")
print("weights (top 10):")
print(weights.sort_values(ascending=False).head(10))

# ------------------------
# 4) rolling monthly 3y max drawdown
# ------------------------
dd_table = compute_rolling_3y_portfolio_mdd(
    prices=prices,
    weights=weights,
    horizon_years=horizon_years,
    start_freq="MS",
    calendar="B",
    require_all_assets=True,   # set False to renormalize when an asset is missing at t0
)

if dd_table.empty:
    print("No valid 3-year windows found (check history length / missing data).")
else:
    worst = dd_table.iloc[0]
    print("\n=== RESULT ===")
    print(f"Worst 3y max drawdown (monthly starts): {worst['max_drawdown']:.2%}")
    print(f"Start:  {pd.to_datetime(worst['start']).date()}")
    print(f"End:    {pd.to_datetime(worst['end']).date()}")
    print(f"Peak:   {pd.to_datetime(worst['peak']).date() if pd.notna(worst['peak']) else None}")
    print(f"Trough: {pd.to_datetime(worst['trough']).date() if pd.notna(worst['trough']) else None}")

    print("\nTop 10 worst windows:")
    print(dd_table.head(10).assign(
        max_drawdown=lambda d: d["max_drawdown"].map(lambda x: f"{x:.2%}")
    ))

writeLog(CONFIG['file']['log'], 'End ' + LOG_TEXT, id=log_id)
