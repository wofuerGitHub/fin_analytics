"""mysql db module"""

#!/usr/bin/python3

"""
File: mysql_db.py
Author: Wolfgang Fuerst
Date: 2025-01-11
Description: Interaction with MYSQL-db based on sqlalchemy 
Issues:
    ...
Updates:
    2025-01-11: added 
Runtime: ...
"""

import pandas as pd
from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.sql import func

configuration = {
    "host": "127.0.0.1",
    "port": "3306",
    "schema": "fmp",
    "user": "fmp",
    "password": "fmp",
    "ssl" : False,
    "ssl_ca" : "",
    "ssl_cert": "",
    "ssl_key": ""
}

def get_configuration():
    """
    Provides the actual configuration.

    Args:
        None

    Raises:
        None

    Returns:
        dict: set of configuration parameters
    """
    return configuration

def set_configuration(
    **kwargs
):
    """
    Updates the configuration.

    Keyword Args:
        host (str, optional): host IP, e.g. 127.0.0.1. Defaults is None.
        port (str, optional): host PORT, e.g. 3306. Defaults is None.
        schema (str, optional): host SCHEMA, e.g. fmp. Defaults is None.
        user (str, optional): host USER, e.g. fmp. Defaults is None.
        password (str, optional): host PASSWORD, e.g. fmp. Defaults is None.
        ssl (boolian, optional): SSL connection, e.g. true. Defaults is None
        ssl_ca (str, optional): Path to SSL ca file, Defaults is None
        ssl_cert (str, optional):
        ssl_key (str, optional):

    Raises:
        None

    Returns:
        dict: set of configuration parameters
    """
    configuration["host"] = kwargs.get('host', configuration["host"])
    configuration["port"] = kwargs.get('port', configuration["port"])
    configuration["schema"] = kwargs.get('schema', configuration["schema"])
    configuration["user"] = kwargs.get('user', configuration["user"])
    configuration["password"] = kwargs.get('password', configuration["password"])
    configuration["ssl"] = kwargs.get('ssl', configuration["ssl"])
    configuration["ssl_ca"] = kwargs.get('ssl_ca', configuration["ssl_ca"])
    configuration["ssl_cert"] = kwargs.get('ssl_cert', configuration["ssl_cert"])
    configuration["ssl_key"] = kwargs.get('ssl_key', configuration["ssl_key"])
    return(get_configuration())

def create_sql_engine(connection_data):
    """
    Create an engine for MySQL connection.
    """
    if not connection_data["ssl"]:
        connection_url = (
            f"mysql+pymysql://{connection_data['user']}:{connection_data['password']}@"
            f"{connection_data['host']}:{connection_data['port']}/{connection_data['schema']}"
        )
    else:
        connection_url = (
            f"mysql+pymysql://{connection_data['user']}:{connection_data['password']}@"
            f"{connection_data['host']}:{connection_data['port']}/{connection_data['schema']}?"
            f"ssl_ca={connection_data['ssl_ca']}&ssl_cert={connection_data['ssl_cert']}&ssl_key={connection_data['ssl_key']}"
        )
    return create_engine(connection_url)

def get_metatable(engine, table: str):
    """
    Get a table from a MySQL database.

    Args:
        engine (sqlalchemy.engine.base.Engine): SQLAlchemy engine.
        table (str): Name of the table to be retrieved.

    Returns:
        sqlalchemy.schema.Table: Table object.
    """
    meta = MetaData()
    meta.reflect(engine)
    return meta.tables[table]

def get_mysql_data(connection, table:str, **kwargs):
    """
    Read a MySQL table into a pandas DataFrame.

    Args:
        table (sqlalchemy.sql.schema.Table): table to be read into a DataFrame.
        columns (array): columns to be read
        filter_updated (str_time): filters for everything newer than given datetime
        order_by (str): column based on to be orderd
        order_desc (bool): True on descending order
        limit (int): rows to read

    Returns:
        dataframe: DataFrame containing the data from the table.
    """
    columns = kwargs.get('columns', table.columns.keys())
    filter_updated = kwargs.get('filter_updated', None)
    order_by = kwargs.get('order_by', None)
    order_desc = kwargs.get('order_desc', False)
    limit = kwargs.get('limit', None)
    stmt = select(*[getattr(table.c, attr) for attr in columns]).limit(limit)
    if filter_updated is not None:
        stmt = stmt.filter(getattr(table.c, 'updated') >= filter_updated)
    if order_by is not None:
        if order_desc is True:
            stmt = stmt.order_by(getattr(table.c, order_by).desc())
        else:
            stmt = stmt.order_by(getattr(table.c, order_by).asc())
    return pd.read_sql_query(stmt, connection)

def get_mysql_data(connection, table:str, **kwargs):
    """
    Read a MySQL table into a pandas DataFrame.

    Args:
        table (sqlalchemy.sql.schema.Table): table to be read into a DataFrame.
        columns (array): columns to be read
        filter_date (str_time): filters for everything newer than a given datetime
        filter_updated (str_time): filters for everything newer than given datetime
        order_by (str): column based on to be orderd
        order_desc (bool): True on descending order
        limit (int): rows to read

    Returns:
        dataframe: DataFrame containing the data from the table.

    Updates:
        2025-01-11 Integration of filter_date for analytics
    """
    columns = kwargs.get('columns', table.columns.keys())
    filter_date = kwargs.get('filter_date', None)
    filter_updated = kwargs.get('filter_updated', None)
    order_by = kwargs.get('order_by', None)
    order_desc = kwargs.get('order_desc', False)
    limit = kwargs.get('limit', None)
    stmt = select(*[getattr(table.c, attr) for attr in columns]).limit(limit)
    if filter_date is not None:
        stmt = stmt.filter(getattr(table.c, 'date') >= filter_date)
    if filter_updated is not None:
        stmt = stmt.filter(getattr(table.c, 'updated') >= filter_updated)
    if order_by is not None:
        if order_desc is True:
            stmt = stmt.order_by(getattr(table.c, order_by).desc())
        else:
            stmt = stmt.order_by(getattr(table.c, order_by).asc())
    return pd.read_sql_query(stmt, connection)

def get_mysql_symbol_list(connection, table:str, **kwargs):
    """
    """
    # column = kwargs.get("column", ["symbol", "currency"])
    # stmt = select(table.c["symbol", "currency"]).group_by(table.c["symbol", "currency"])
    columns = kwargs.get('columns', ['symbol', 'currency'])
    # stmt = select(table.c[*columns]).group_by(table.c[*columns])
    stmt = select(*[getattr(table.c, attr) for attr in columns]).group_by(*[getattr(table.c, attr) for attr in columns])
    # stmt = select(table.c["symbol", "currency"]).group_by(table.c["symbol", "currency"])
    return pd.read_sql_query(stmt, connection)

def put_dict_to_mysql(connection, table: str, data_dict: dict, unique_keys: list, **kwargs):
    """
    Write a dictionary to a MySQL table.

    Args:
        connection (sqlalchemy.engine.base.Connection): Connection to MySQL database.
        table (str): Name of the table to which the data will be written.
        data_dict (dict): Dictionary of data to be written to the table.
        unique_keys (list): List of column names that will be used as unique keys for the table.
    
    Keyword Args:
        update_timestamp (bool): True if updated is filled with actual time
        commitment_rate (int): number for items to transmit per block

    Raise:
        Exception: If writing to database fails.

    Returns:
    None
    """
    update_timestamp = kwargs.get('update_timestamp', True)
    commitment_rate = kwargs.get("commitment_rate", 10000)

    if isinstance(data_dict, dict): data_dict = [data_dict] # single dict put in an array

    # fix sqlalchemy.exc.CompileError: Unconsumed column names: column_name
    column_names = table.columns.keys()
    data_dict = [{k: v for k, v in d.items() if k in column_names} for d in data_dict]

    if isinstance(data_dict, list):
        if len(data_dict) >= 1:
            i_max = len(data_dict)-1
            for i, data_set in enumerate(data_dict):
                update_data_set = {k: v for k, v in data_set.items() if k not in unique_keys}
                if update_timestamp:
                    stmt = insert(table).values(data_set).on_duplicate_key_update(
                        **update_data_set, updated = func.current_timestamp())
                else:
                    stmt = insert(table).values(data_set).on_duplicate_key_update(
                        **update_data_set)
                try:
                    connection.execute(stmt)
                    if i % commitment_rate == 0 or i == i_max:
                        connection.commit()
                        print('commit done')
                except:
                    connection.rollback()
                    raise Exception("Writing to database failed and was rolled back")
        else:
            raise Exception("No data to write")

def put_dataframe_to_mysql(connection, table: str, data_frame: dict, unique_keys: list, **kwargs):
    """
    Write a dataframe to a MySQL table.

    Args:
        connection (sqlalchemy.engine.base.Connection): Connection to MySQL database.
        table (str): Name of the table to which the data will be written.
        data_frame (dataframe): DataFrame of data to be written to the table.
        unique_keys (list): List of column names that will be used as unique keys for the table.
    
    Keyword Args:
        update_timestamp (bool): True if updated is filled with actual time
        commitment_rate (int): number for items to transmit per block

    Raise:
        Exception: If writing to database fails.

    Returns:
        None

    Updates:
        2025-01-11: Initial version
    """
    data_frame = data_frame.astype(str)                 # convert all to str
    data_dict = data_frame.to_dict(orient='records')    # convert data_frame to data_dict

    data_to_insert = []                                 # generate new dict without invalid 'nan' or 'None'
    for i, val in enumerate(data_dict):
        keys = [key for key, value in val.items() if value == 'nan' or value == 'None']
        for key in keys:
            val.pop(key, None)
        data_to_insert.append(val)

    put_dict_to_mysql(connection, table, data_to_insert, unique_keys, **kwargs)
