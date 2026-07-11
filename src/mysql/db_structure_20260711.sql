CREATE DATABASE  IF NOT EXISTS `fin` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `fin`;
-- MySQL dump 10.13  Distrib 8.0.42, for macos15 (arm64)
--
-- Host: localhost    Database: fin
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `_reference_map`
--

DROP TABLE IF EXISTS `_reference_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `_reference_map` (
  `symbol` varchar(255) NOT NULL,
  `symbol_fundamental` varchar(255) DEFAULT NULL,
  `isin` varchar(12) DEFAULT NULL,
  `currency` varchar(3) NOT NULL,
  `companyName` varchar(255) DEFAULT NULL,
  `industry` varchar(255) DEFAULT NULL,
  `sector` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `active` tinyint NOT NULL DEFAULT '1',
  `longTimeSerie` tinyint NOT NULL DEFAULT '1',
  `stream` tinyint NOT NULL DEFAULT '1',
  `comment` text,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`symbol`),
  UNIQUE KEY `symbol_UNIQUE` (`symbol`),
  UNIQUE KEY `isin_UNIQUE` (`isin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='reference for all the time-series quotes and fundamentals to be queried and merged\n\nsymbol -> ts\nsymbol_fundamental -> fundamental\nactive -> if ts should be queried\nlongTimeSerie -> if ts should get 30y data\nstream -> if ts should get streamed';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `active_security_quote_freshness`
--

DROP TABLE IF EXISTS `active_security_quote_freshness`;
/*!50001 DROP VIEW IF EXISTS `active_security_quote_freshness`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `active_security_quote_freshness` AS SELECT 
 1 AS `symbol`,
 1 AS `companyName`,
 1 AS `newest_date`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `annotations`
--

DROP TABLE IF EXISTS `annotations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `annotations` (
  `pk` int NOT NULL,
  `date` date NOT NULL,
  `text` varchar(255) NOT NULL,
  `tags` varchar(50) NOT NULL,
  `background` text,
  `link` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`pk`),
  UNIQUE KEY `pk_UNIQUE` (`pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `edcbps_eur`
--

DROP TABLE IF EXISTS `edcbps_eur`;
/*!50001 DROP VIEW IF EXISTS `edcbps_eur`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `edcbps_eur` AS SELECT 
 1 AS `date`,
 1 AS `symbol`,
 1 AS `reportedCurrency`,
 1 AS `calendarYear`,
 1 AS `period`,
 1 AS `eps_eur`,
 1 AS `dps_eur`,
 1 AS `cps_eur`,
 1 AS `bps_eur`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `eps_analyzed`
--

DROP TABLE IF EXISTS `eps_analyzed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eps_analyzed` (
  `symbol` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `type` text NOT NULL,
  `risk` tinyint(1) NOT NULL,
  `rsq` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `sevenYears` double DEFAULT NULL,
  `fifteenYears` double DEFAULT NULL,
  `twentyYears` double DEFAULT NULL,
  `interest` double DEFAULT NULL,
  `doubled` double DEFAULT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`symbol`,`date`,`created`),
  UNIQUE KEY `symbol_date` (`symbol`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eps_analyzed_raw`
--

DROP TABLE IF EXISTS `eps_analyzed_raw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eps_analyzed_raw` (
  `symbol` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `eps` double DEFAULT NULL,
  `epsStar` double DEFAULT NULL,
  `growth` double DEFAULT NULL,
  `growthStar` double DEFAULT NULL,
  `lastEight` double DEFAULT NULL,
  `lastX` double DEFAULT NULL,
  `trend` double DEFAULT NULL,
  `sevenYearAvg` double DEFAULT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`symbol`,`date`,`created`),
  UNIQUE KEY `symbol_date_created` (`symbol`,`date`,`created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eur_companykeystats`
--

DROP TABLE IF EXISTS `eur_companykeystats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eur_companykeystats` (
  `symbol` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price` double DEFAULT NULL,
  `mktCap` double DEFAULT NULL,
  `lastDiv` double DEFAULT NULL,
  `min` double DEFAULT NULL,
  `max` double DEFAULT NULL,
  `range` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `companyName` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `currency` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `isin` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `exchange` mediumtext,
  `exchangeShortName` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `industry` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `website` mediumtext,
  `description` mediumtext,
  `ceo` mediumtext,
  `sector` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `country` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `fullTimeEmployees` mediumtext,
  `phone` mediumtext,
  `address` mediumtext,
  `city` mediumtext,
  `state` mediumtext,
  `zip` mediumtext,
  `image` mediumtext,
  `ipoDate` mediumtext,
  `defaultImage` tinyint(1) DEFAULT NULL,
  `isEtf` tinyint(1) DEFAULT NULL,
  `isActivelyTrading` tinyint(1) DEFAULT NULL,
  `isAdr` tinyint(1) DEFAULT NULL,
  `isFund` tinyint(1) DEFAULT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`symbol`),
  UNIQUE KEY `symbol_UNIQUE` (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eur_fun`
--

DROP TABLE IF EXISTS `eur_fun`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eur_fun` (
  `date` date NOT NULL,
  `symbol` varchar(255) NOT NULL,
  `calendarYear` text NOT NULL,
  `period` text NOT NULL,
  `grossProfitRatio` double DEFAULT NULL,
  `researchAndDevelopmentRatio` double DEFAULT NULL,
  `interestExpenseRatio` double DEFAULT NULL,
  `eps` double DEFAULT NULL COMMENT 'eps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),(`is_netIncome` / `is_weightedAverageShsOut`),NULL)\ndps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),(-`cs_dividendsPaid` / `is_weightedAverageShsOut`),NULL)\ncps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),(`cs_operatingCashFlow` / `is_weightedAverageShsOut`),NULL)\nbps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),((`bs_totalStockholdersEquity`-bs_preferredStock) / `is_weightedAverageShsOut`),NULL)\n',
  `dps` double DEFAULT NULL COMMENT 'eps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),(`is_netIncome` / `is_weightedAverageShsOut`),NULL)\\n\ndps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),(-`cs_dividendsPaid` / `is_weightedAverageShsOut`),NULL)\\n\ncps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),(`cs_operatingCashFlow` / `is_weightedAverageShsOut`),NULL)\\n\nbps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),((`bs_totalStockholdersEquity`-bs_preferredStock) / `is_weightedAverageShsOut`),NULL)',
  `cps` double DEFAULT NULL COMMENT 'eps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),(`is_netIncome` / `is_weightedAverageShsOut`),NULL)\\\\n\\n\ndps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),(-`cs_dividendsPaid` / `is_weightedAverageShsOut`),NULL)\\\\n\\n\ncps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),(`cs_operatingCashFlow` / `is_weightedAverageShsOut`),NULL)\\\\n\\n\nbps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),((`bs_totalStockholdersEquity`-bs_preferredStock) / `is_weightedAverageShsOut`),NULL)',
  `bps` double DEFAULT NULL COMMENT 'eps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),(`is_netIncome` / `is_weightedAverageShsOut`),NULL)\\\\ndps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),(-`cs_dividendsPaid` / `is_weightedAverageShsOut`),NULL)\\\\ncps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),(`cs_operatingCashFlow` / `is_weightedAverageShsOut`),NULL)\\\\n\nbps: if(((`is_weightedAverageShsOut` is not null) and (`is_weightedAverageShsOut` >= 1)),((`bs_totalStockholdersEquity`-bs_preferredStock) / `is_weightedAverageShsOut`),NULL)',
  `currency` varchar(3) DEFAULT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `manual` text,
  PRIMARY KEY (`date`,`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `eur_fun_quote`
--

DROP TABLE IF EXISTS `eur_fun_quote`;
/*!50001 DROP VIEW IF EXISTS `eur_fun_quote`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `eur_fun_quote` AS SELECT 
 1 AS `symbol`,
 1 AS `symbol_fundamental`,
 1 AS `date`,
 1 AS `calendarYear`,
 1 AS `grossProfitRatio`,
 1 AS `researchAndDevelopmentRatio`,
 1 AS `interestExpenseRatio`,
 1 AS `eps`,
 1 AS `dps`,
 1 AS `cps`,
 1 AS `bps`,
 1 AS `close`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `eur_ts_fx`
--

DROP TABLE IF EXISTS `eur_ts_fx`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eur_ts_fx` (
  `date` date NOT NULL,
  `symbol` varchar(255) NOT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double NOT NULL,
  `currency` varchar(3) NOT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`date`,`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='FX: data (in EUR) from raw_ts_fx';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eur_ts_quote`
--

DROP TABLE IF EXISTS `eur_ts_quote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eur_ts_quote` (
  `date` date NOT NULL,
  `symbol` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `close` double NOT NULL,
  `eps` double GENERATED ALWAYS AS (if((`per` is not null),(`close` / `per`),NULL)) VIRTUAL,
  `per` double DEFAULT NULL,
  `currency` varchar(3) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`date`,`symbol`),
  KEY `idx_eur_ts_quote_symbol_date` (`symbol`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Purpose: Stores historical security OHLC prices normalized to EUR, including derived EPS and PER fields. \nGrain: One row per security and trading date. \nSource: raw_ts_quote combined with eur_ts_fx. \nLifecycle: Persistent historical data.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `my_portfolio`
--

DROP TABLE IF EXISTS `my_portfolio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `my_portfolio` (
  `symbol` varchar(255) NOT NULL,
  `isin` varchar(12) DEFAULT NULL,
  `companyName` text,
  `type_1` varchar(45) DEFAULT NULL,
  `type_2` varchar(45) DEFAULT NULL,
  `ing` double DEFAULT '0',
  `ibkr` double DEFAULT '0',
  `idea` double DEFAULT '0',
  `all` double GENERATED ALWAYS AS (((`ing` + `ibkr`) + `idea`)) VIRTUAL,
  `risk` varchar(1) DEFAULT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`symbol`),
  UNIQUE KEY `symbol_UNIQUE` (`symbol`),
  UNIQUE KEY `isin_UNIQUE` (`isin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `my_portfolio_calculated`
--

DROP TABLE IF EXISTS `my_portfolio_calculated`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `my_portfolio_calculated` (
  `symbol` varchar(255) NOT NULL,
  `isin` varchar(12) DEFAULT NULL,
  `companyName` text,
  `all` double DEFAULT NULL,
  `perf` double DEFAULT NULL,
  `vola` double DEFAULT NULL,
  `sr` double DEFAULT NULL,
  `epr` double DEFAULT NULL,
  `bpr` double DEFAULT NULL,
  `start_weight` double DEFAULT NULL,
  `end_weight` double DEFAULT NULL,
  `opt_sr` double DEFAULT NULL,
  `opt_perf_epr` double DEFAULT NULL,
  `opt_perf_bpr` double DEFAULT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`symbol`),
  UNIQUE KEY `symbol_UNIQUE` (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `my_portfolio_calculated_ext`
--

DROP TABLE IF EXISTS `my_portfolio_calculated_ext`;
/*!50001 DROP VIEW IF EXISTS `my_portfolio_calculated_ext`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `my_portfolio_calculated_ext` AS SELECT 
 1 AS `symbol`,
 1 AS `isin`,
 1 AS `companyName`,
 1 AS `perf`,
 1 AS `vola`,
 1 AS `sr`,
 1 AS `epr`,
 1 AS `bpr`,
 1 AS `end_weight`,
 1 AS `opt_sr`,
 1 AS `opt_perf_epr`,
 1 AS `opt_perf_bpr`,
 1 AS `grossProfitRatio`,
 1 AS `researchAndDevelopmentRatio`,
 1 AS `interestExpenseRatio`,
 1 AS `per_mean`,
 1 AS `pdr_mean`,
 1 AS `pcr_mean`,
 1 AS `pbr_mean`,
 1 AS `ppr_est`,
 1 AS `corr_idx`,
 1 AS `perf_idx`,
 1 AS `vola_idx`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `my_portfolio_calculated_ext_2`
--

DROP TABLE IF EXISTS `my_portfolio_calculated_ext_2`;
/*!50001 DROP VIEW IF EXISTS `my_portfolio_calculated_ext_2`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `my_portfolio_calculated_ext_2` AS SELECT 
 1 AS `symbol`,
 1 AS `isin`,
 1 AS `companyName`,
 1 AS `industry`,
 1 AS `sector`,
 1 AS `country`,
 1 AS `perf`,
 1 AS `vola`,
 1 AS `sr`,
 1 AS `epr`,
 1 AS `bpr`,
 1 AS `end_weight`,
 1 AS `opt_sr`,
 1 AS `opt_perf_epr`,
 1 AS `opt_perf_bpr`,
 1 AS `grossProfitRatio`,
 1 AS `researchAndDevelopmentRatio`,
 1 AS `interestExpenseRatio`,
 1 AS `per_mean`,
 1 AS `pdr_mean`,
 1 AS `pcr_mean`,
 1 AS `pbr_mean`,
 1 AS `ppr_est`,
 1 AS `corr_idx`,
 1 AS `perf_idx`,
 1 AS `vola_idx`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `my_portfolio_calculated_ext_mat`
--

DROP TABLE IF EXISTS `my_portfolio_calculated_ext_mat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `my_portfolio_calculated_ext_mat` (
  `symbol` varchar(255) NOT NULL,
  `isin` varchar(12) DEFAULT NULL,
  `companyName` text,
  `perf` double DEFAULT NULL,
  `vola` double DEFAULT NULL,
  `sr` double DEFAULT NULL,
  `epr` double DEFAULT NULL,
  `bpr` double DEFAULT NULL,
  `end_weight` double DEFAULT NULL,
  `opt_sr` double DEFAULT NULL,
  `opt_perf_epr` double DEFAULT NULL,
  `opt_perf_bpr` double DEFAULT NULL,
  `grossProfitRatio` double DEFAULT NULL,
  `researchAndDevelopmentRatio` double DEFAULT NULL,
  `interestExpenseRatio` double DEFAULT NULL,
  `per_mean` double DEFAULT NULL,
  `pdr_mean` double DEFAULT NULL,
  `pcr_mean` double DEFAULT NULL,
  `pbr_mean` double DEFAULT NULL,
  `ppr_est` double DEFAULT NULL,
  `corr_idx` double DEFAULT NULL,
  `perf_idx` double DEFAULT NULL,
  `vola_idx` double DEFAULT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `my_portfolio_overview`
--

DROP TABLE IF EXISTS `my_portfolio_overview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `my_portfolio_overview` (
  `name` varchar(255) NOT NULL,
  `perf` double DEFAULT NULL,
  `vola` double DEFAULT NULL,
  `sr` double DEFAULT NULL,
  `epr` double DEFAULT NULL,
  `per` double DEFAULT NULL,
  `bpr` double DEFAULT NULL,
  `pbr` double DEFAULT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`name`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `object_documentation`
--

DROP TABLE IF EXISTS `object_documentation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `object_documentation` (
  `object_schema` varchar(64) NOT NULL,
  `object_name` varchar(64) NOT NULL,
  `object_type` enum('TABLE','VIEW','PROCEDURE','FUNCTION') NOT NULL,
  `purpose` text NOT NULL,
  `grain` text,
  `source` text,
  `lifecycle` text,
  `notes` text,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`object_schema`,`object_name`,`object_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Stores business and technical documentation for database tables and views.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `quote_eur`
--

DROP TABLE IF EXISTS `quote_eur`;
/*!50001 DROP VIEW IF EXISTS `quote_eur`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `quote_eur` AS SELECT 
 1 AS `date`,
 1 AS `symbol`,
 1 AS `open`,
 1 AS `high`,
 1 AS `low`,
 1 AS `close`,
 1 AS `eps`,
 1 AS `currency`,
 1 AS `created`,
 1 AS `updated`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `quote_eur_last`
--

DROP TABLE IF EXISTS `quote_eur_last`;
/*!50001 DROP VIEW IF EXISTS `quote_eur_last`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `quote_eur_last` AS SELECT 
 1 AS `date`,
 1 AS `symbol`,
 1 AS `open`,
 1 AS `high`,
 1 AS `low`,
 1 AS `close`,
 1 AS `eps`,
 1 AS `currency`,
 1 AS `created`,
 1 AS `checked`,
 1 AS `updated`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `referencedata`
--

DROP TABLE IF EXISTS `referencedata`;
/*!50001 DROP VIEW IF EXISTS `referencedata`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `referencedata` AS SELECT 
 1 AS `symbol`,
 1 AS `symbol_fundamental`,
 1 AS `isin`,
 1 AS `currency`,
 1 AS `companyName`,
 1 AS `industry`,
 1 AS `sector`,
 1 AS `country`,
 1 AS `longTimeSerie`,
 1 AS `comment`,
 1 AS `created`,
 1 AS `updated`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `security_valuation_interest`
--

DROP TABLE IF EXISTS `security_valuation_interest`;
/*!50001 DROP VIEW IF EXISTS `security_valuation_interest`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `security_valuation_interest` AS SELECT 
 1 AS `symbol`,
 1 AS `company_name`,
 1 AS `eps_growth`,
 1 AS `interest_date`,
 1 AS `per_mean`,
 1 AS `last_per`,
 1 AS `per_date`,
 1 AS `per_interest`,
 1 AS `pbr_mean`,
 1 AS `last_pbr`,
 1 AS `price_date`,
 1 AS `fundamental_date`,
 1 AS `pbr_interest`,
 1 AS `dividend`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `show_all_active_assets_with_last_quote_and_fundamental`
--

DROP TABLE IF EXISTS `show_all_active_assets_with_last_quote_and_fundamental`;
/*!50001 DROP VIEW IF EXISTS `show_all_active_assets_with_last_quote_and_fundamental`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `show_all_active_assets_with_last_quote_and_fundamental` AS SELECT 
 1 AS `companyName`,
 1 AS `isin`,
 1 AS `symbol`,
 1 AS `max_date`,
 1 AS `symbol_fun`,
 1 AS `max_date_fun`,
 1 AS `max_calendar_year`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `truevalue_raw`
--

DROP TABLE IF EXISTS `truevalue_raw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `truevalue_raw` (
  `symbol` text,
  `date` date DEFAULT NULL,
  `value` double DEFAULT NULL,
  `inf_rate` double DEFAULT NULL,
  `inf_value` double DEFAULT NULL,
  `currency` text,
  `value_avg` double DEFAULT NULL,
  `inf_rate_avg` double DEFAULT NULL,
  `inf_value_avg` double DEFAULT NULL,
  `tenYearPerformance` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `validation_board`
--

DROP TABLE IF EXISTS `validation_board`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `validation_board` (
  `date` datetime NOT NULL,
  `symbol` varchar(255) NOT NULL,
  `companyName` varchar(255) DEFAULT NULL,
  `grossProfitRatio` double DEFAULT NULL,
  `researchAndDevelopmentRatio` double DEFAULT NULL,
  `interestExpenseRatio` double DEFAULT NULL,
  `per_est` double DEFAULT NULL,
  `per_mean` double DEFAULT NULL,
  `pdr_est` double DEFAULT NULL,
  `pdr_mean` double DEFAULT NULL,
  `pcr_est` double DEFAULT NULL,
  `pcr_mean` double DEFAULT NULL,
  `pbr_est` double DEFAULT NULL,
  `pbr_mean` double DEFAULT NULL,
  `ppr_est` double DEFAULT NULL,
  `ppr_mean` double DEFAULT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`symbol`),
  UNIQUE KEY `symbol_UNIQUE` (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `validation_correlation`
--

DROP TABLE IF EXISTS `validation_correlation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `validation_correlation` (
  `symbol_ij` varchar(255) NOT NULL,
  `symbol_i` text,
  `perf` double DEFAULT NULL,
  `vola` double DEFAULT NULL,
  `sr` double DEFAULT NULL,
  `symbol_j` text,
  `corr_ij` double DEFAULT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`symbol_ij`),
  UNIQUE KEY `symbol_ij_UNIQUE` (`symbol_ij`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `validation_manual`
--

DROP TABLE IF EXISTS `validation_manual`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `validation_manual` (
  `symbol` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `fairValue_DCF` double DEFAULT NULL,
  `businessCapitalPreservationStrength` double DEFAULT NULL,
  `shareholderCapitalPreservationStrength` double DEFAULT NULL,
  `riskClass` double DEFAULT NULL COMMENT 'A number 1 (low risk) -10 (high risk)',
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`symbol`,`date`,`created`),
  UNIQUE KEY `symbol_date` (`symbol`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `validation_optimization`
--

DROP TABLE IF EXISTS `validation_optimization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `validation_optimization` (
  `isin` varchar(12) NOT NULL,
  `companyName` text,
  `all` double DEFAULT NULL,
  `share` double DEFAULT NULL,
  `perf_all` double DEFAULT NULL,
  `vola_all` double DEFAULT NULL,
  `sr_all` double DEFAULT NULL,
  `recommended_min_vola` double DEFAULT NULL,
  `recommended_max_sr` double DEFAULT NULL,
  `one_percent_perf` double DEFAULT NULL,
  `one_percent_vola` double DEFAULT NULL,
  `perf_min_vola_rec` double DEFAULT NULL,
  `vola_min_vola_rec` double DEFAULT NULL,
  `sr_min_vola_rec` double DEFAULT NULL,
  `sector` bigint DEFAULT NULL,
  `change_perf` double DEFAULT NULL,
  `change_vola` double DEFAULT NULL,
  `change_sensitivity` double DEFAULT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`isin`),
  UNIQUE KEY `isin_UNIQUE` (`isin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `validation_pvs`
--

DROP TABLE IF EXISTS `validation_pvs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `validation_pvs` (
  `symbol` varchar(255) NOT NULL,
  `max_date` date DEFAULT NULL,
  `min_date` date DEFAULT NULL,
  `period` bigint NOT NULL,
  `perf` double DEFAULT NULL,
  `vola` double DEFAULT NULL,
  `sr` double DEFAULT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`symbol`,`period`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `validation_value`
--

DROP TABLE IF EXISTS `validation_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `validation_value` (
  `companyName` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `sector` varchar(255) DEFAULT NULL,
  `symbol` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `type` text NOT NULL,
  `rsq` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `sevenYears` double DEFAULT NULL,
  `fifteenYears` double DEFAULT NULL,
  `interest` double DEFAULT NULL,
  `doubled` double DEFAULT NULL,
  `ratio` double DEFAULT NULL,
  `pbr` double DEFAULT NULL,
  `pbr_est` double DEFAULT NULL,
  `per_est` double DEFAULT NULL,
  `grossProfitRatio` double DEFAULT NULL,
  `researchAndDevelopmentRatio` double DEFAULT NULL,
  `interestExpenseRatio` double DEFAULT NULL,
  `fairValue_DCF` double DEFAULT NULL,
  `businessCapitalPreservationStrength` double DEFAULT NULL,
  `shareholderCapitalPreservationStrength` double DEFAULT NULL,
  `riskClass` double DEFAULT NULL COMMENT 'A number 1 (low risk) -10 (high risk)',
  `manualDate` date,
  `updated` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `validation_value_view`
--

DROP TABLE IF EXISTS `validation_value_view`;
/*!50001 DROP VIEW IF EXISTS `validation_value_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `validation_value_view` AS SELECT 
 1 AS `companyName`,
 1 AS `country`,
 1 AS `sector`,
 1 AS `symbol`,
 1 AS `date`,
 1 AS `type`,
 1 AS `rsq`,
 1 AS `close`,
 1 AS `sevenYears`,
 1 AS `fifteenYears`,
 1 AS `interest`,
 1 AS `doubled`,
 1 AS `ratio`,
 1 AS `pbr`,
 1 AS `pbr_est`,
 1 AS `per_est`,
 1 AS `grossProfitRatio`,
 1 AS `researchAndDevelopmentRatio`,
 1 AS `interestExpenseRatio`,
 1 AS `fairValue_DCF`,
 1 AS `businessCapitalPreservationStrength`,
 1 AS `shareholderCapitalPreservationStrength`,
 1 AS `riskClass`,
 1 AS `manualDate`,
 1 AS `updated`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `validation_value_view_20260527`
--

DROP TABLE IF EXISTS `validation_value_view_20260527`;
/*!50001 DROP VIEW IF EXISTS `validation_value_view_20260527`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `validation_value_view_20260527` AS SELECT 
 1 AS `companyName`,
 1 AS `country`,
 1 AS `sector`,
 1 AS `symbol`,
 1 AS `date`,
 1 AS `type`,
 1 AS `rsq`,
 1 AS `close`,
 1 AS `sevenYears`,
 1 AS `fifteenYears`,
 1 AS `interest`,
 1 AS `doubled`,
 1 AS `ratio`,
 1 AS `pbr`,
 1 AS `pbr_est`,
 1 AS `per_est`,
 1 AS `grossProfitRatio`,
 1 AS `researchAndDevelopmentRatio`,
 1 AS `interestExpenseRatio`,
 1 AS `updated`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `active_security_quote_freshness`
--

/*!50001 DROP VIEW IF EXISTS `active_security_quote_freshness`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `active_security_quote_freshness` AS select `r`.`symbol` AS `symbol`,`r`.`companyName` AS `companyName`,`q`.`newest_date` AS `newest_date` from (`_reference_map` `r` left join (select `eur_ts_quote`.`symbol` AS `symbol`,max(`eur_ts_quote`.`date`) AS `newest_date` from `eur_ts_quote` group by `eur_ts_quote`.`symbol`) `q` on((`q`.`symbol` = `r`.`symbol`))) where (`r`.`active` = 1) order by `q`.`newest_date` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `edcbps_eur`
--

/*!50001 DROP VIEW IF EXISTS `edcbps_eur`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb3 */;
/*!50001 SET character_set_results     = utf8mb3 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`fin_backup`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `edcbps_eur` AS select 1 AS `date`,1 AS `symbol`,1 AS `reportedCurrency`,1 AS `calendarYear`,1 AS `period`,1 AS `eps_eur`,1 AS `dps_eur`,1 AS `cps_eur`,1 AS `bps_eur` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `eur_fun_quote`
--

/*!50001 DROP VIEW IF EXISTS `eur_fun_quote`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb3 */;
/*!50001 SET character_set_results     = utf8mb3 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`fin_backup`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `eur_fun_quote` AS select 1 AS `symbol`,1 AS `symbol_fundamental`,1 AS `date`,1 AS `calendarYear`,1 AS `grossProfitRatio`,1 AS `researchAndDevelopmentRatio`,1 AS `interestExpenseRatio`,1 AS `eps`,1 AS `dps`,1 AS `cps`,1 AS `bps`,1 AS `close` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `my_portfolio_calculated_ext`
--

/*!50001 DROP VIEW IF EXISTS `my_portfolio_calculated_ext`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `my_portfolio_calculated_ext` AS select `a`.`symbol` AS `symbol`,`a`.`isin` AS `isin`,`a`.`companyName` AS `companyName`,`a`.`perf` AS `perf`,`a`.`vola` AS `vola`,`a`.`sr` AS `sr`,`a`.`epr` AS `epr`,`a`.`bpr` AS `bpr`,`a`.`end_weight` AS `end_weight`,`a`.`opt_sr` AS `opt_sr`,`a`.`opt_perf_epr` AS `opt_perf_epr`,`a`.`opt_perf_bpr` AS `opt_perf_bpr`,(case when ((`a`.`symbol` = 'IVV') or (`a`.`symbol` = 'EXSA.DE')) then 0.4 else greatest(`b`.`grossProfitRatio`,0) end) AS `grossProfitRatio`,(case when ((`a`.`symbol` = 'IVV') or (`a`.`symbol` = 'EXSA.DE')) then 0.06 else greatest(`b`.`researchAndDevelopmentRatio`,0) end) AS `researchAndDevelopmentRatio`,(case when ((`a`.`symbol` = 'IVV') or (`a`.`symbol` = 'EXSA.DE')) then 0.03 else greatest(`b`.`interestExpenseRatio`,0) end) AS `interestExpenseRatio`,`b`.`per_mean` AS `per_mean`,`b`.`pdr_mean` AS `pdr_mean`,`b`.`pcr_mean` AS `pcr_mean`,`b`.`pbr_mean` AS `pbr_mean`,`b`.`ppr_est` AS `ppr_est`,(case when (`a`.`symbol` = 'IVV') then 1 else `c`.`corr_ij` end) AS `corr_idx`,(select `my_portfolio_calculated`.`perf` from `my_portfolio_calculated` where (`my_portfolio_calculated`.`symbol` = 'IVV')) AS `perf_idx`,(select `my_portfolio_calculated`.`vola` from `my_portfolio_calculated` where (`my_portfolio_calculated`.`symbol` = 'IVV')) AS `vola_idx` from ((`my_portfolio_calculated` `a` left join `validation_board` `b` on((`a`.`symbol` = `b`.`symbol`))) left join (select if((`d`.`symbol_i` <> 'IVV'),`d`.`symbol_i`,`d`.`symbol_j`) AS `symbol`,`d`.`symbol_ij` AS `symbol_ij`,`d`.`symbol_i` AS `symbol_i`,`d`.`perf` AS `perf`,`d`.`vola` AS `vola`,`d`.`sr` AS `sr`,`d`.`symbol_j` AS `symbol_j`,`d`.`corr_ij` AS `corr_ij`,`d`.`created` AS `created`,`d`.`updated` AS `updated` from `validation_correlation` `d` where (`d`.`symbol_i` in (select `my_portfolio`.`symbol` from `my_portfolio`) and `d`.`symbol_j` in (select `my_portfolio`.`symbol` from `my_portfolio`) and (`d`.`symbol_ij` like '%IVV%'))) `c` on((`a`.`symbol` = `c`.`symbol`))) where (`a`.`all` <> 1) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `my_portfolio_calculated_ext_2`
--

/*!50001 DROP VIEW IF EXISTS `my_portfolio_calculated_ext_2`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `my_portfolio_calculated_ext_2` AS select `a`.`symbol` AS `symbol`,`a`.`isin` AS `isin`,`a`.`companyName` AS `companyName`,`d`.`industry` AS `industry`,`d`.`sector` AS `sector`,`d`.`country` AS `country`,`a`.`perf` AS `perf`,`a`.`vola` AS `vola`,`a`.`sr` AS `sr`,`a`.`epr` AS `epr`,`a`.`bpr` AS `bpr`,`a`.`end_weight` AS `end_weight`,`a`.`opt_sr` AS `opt_sr`,`a`.`opt_perf_epr` AS `opt_perf_epr`,`a`.`opt_perf_bpr` AS `opt_perf_bpr`,(case when (`a`.`symbol` in ('IVV','EXSA.DE')) then 0.4 else greatest(`b`.`grossProfitRatio`,0) end) AS `grossProfitRatio`,(case when (`a`.`symbol` in ('IVV','EXSA.DE')) then 0.06 else greatest(`b`.`researchAndDevelopmentRatio`,0) end) AS `researchAndDevelopmentRatio`,(case when (`a`.`symbol` in ('IVV','EXSA.DE')) then 0.03 else greatest(`b`.`interestExpenseRatio`,0) end) AS `interestExpenseRatio`,`b`.`per_mean` AS `per_mean`,`b`.`pdr_mean` AS `pdr_mean`,`b`.`pcr_mean` AS `pcr_mean`,`b`.`pbr_mean` AS `pbr_mean`,`b`.`ppr_est` AS `ppr_est`,(case when (`a`.`symbol` = 'IVV') then 1 else `c`.`corr_ij` end) AS `corr_idx`,`idx`.`perf` AS `perf_idx`,`idx`.`vola` AS `vola_idx` from ((((`my_portfolio_calculated` `a` left join `validation_board` `b` on((`b`.`symbol` = `a`.`symbol`))) left join `my_portfolio_calculated` `idx` on((`idx`.`symbol` = 'IVV'))) left join (select `a`.`symbol` AS `symbol`,`b`.`corr_ij` AS `corr_ij` from (`my_portfolio_calculated` `a` left join `validation_correlation` `b` on(((`a`.`symbol` = `b`.`symbol_i`) and (`b`.`symbol_j` = 'IVV')))) where (`b`.`corr_ij` is not null) union select `a`.`symbol` AS `symbol`,`b`.`corr_ij` AS `corr_ij` from (`my_portfolio_calculated` `a` left join `validation_correlation` `b` on(((`a`.`symbol` = `b`.`symbol_j`) and (`b`.`symbol_i` = 'IVV')))) where (`b`.`corr_ij` is not null) union select 'IVV' AS `symbol`,1 AS `corr_ij`) `c` on((`c`.`symbol` = `a`.`symbol`))) left join `_reference_map` `d` on((`a`.`symbol` = `d`.`symbol`))) where (`a`.`all` <> 1) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `quote_eur`
--

/*!50001 DROP VIEW IF EXISTS `quote_eur`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `quote_eur` AS select `b`.`date` AS `date`,`a`.`symbol` AS `symbol`,`b`.`open` AS `open`,`b`.`high` AS `high`,`b`.`low` AS `low`,`b`.`close` AS `close`,`b`.`eps` AS `eps`,`b`.`currency` AS `currency`,`b`.`created` AS `created`,`b`.`updated` AS `updated` from (`_reference_map` `a` left join `eur_ts_quote` `b` on((`a`.`symbol` = `b`.`symbol`))) order by `b`.`date` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `quote_eur_last`
--

/*!50001 DROP VIEW IF EXISTS `quote_eur_last`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `quote_eur_last` AS select `b`.`date` AS `date`,`b`.`symbol` AS `symbol`,`b`.`open` AS `open`,`b`.`high` AS `high`,`b`.`low` AS `low`,`b`.`close` AS `close`,`b`.`eps` AS `eps`,`b`.`currency` AS `currency`,`b`.`created` AS `created`,`b`.`updated` AS `checked`,`b`.`updated` AS `updated` from ((select `quote_eur`.`symbol` AS `symbol`,max(`quote_eur`.`date`) AS `date` from `quote_eur` group by `quote_eur`.`symbol`) `a` left join `quote_eur` `b` on(((`a`.`symbol` = `b`.`symbol`) and (`a`.`date` = `b`.`date`)))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `referencedata`
--

/*!50001 DROP VIEW IF EXISTS `referencedata`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `referencedata` AS select `_reference_map`.`symbol` AS `symbol`,`_reference_map`.`symbol_fundamental` AS `symbol_fundamental`,`_reference_map`.`isin` AS `isin`,`_reference_map`.`currency` AS `currency`,`_reference_map`.`companyName` AS `companyName`,`_reference_map`.`industry` AS `industry`,`_reference_map`.`sector` AS `sector`,`_reference_map`.`country` AS `country`,`_reference_map`.`longTimeSerie` AS `longTimeSerie`,`_reference_map`.`comment` AS `comment`,`_reference_map`.`created` AS `created`,`_reference_map`.`updated` AS `updated` from `_reference_map` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `security_valuation_interest`
--

/*!50001 DROP VIEW IF EXISTS `security_valuation_interest`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY INVOKER */
/*!50001 VIEW `security_valuation_interest` AS with `latest_interest` as (select `x`.`symbol` AS `symbol`,`x`.`interest` AS `interest`,`x`.`date` AS `interest_date` from (select `vv`.`symbol` AS `symbol`,`vv`.`interest` AS `interest`,`vv`.`date` AS `date`,row_number() OVER (PARTITION BY `vv`.`symbol` ORDER BY `vv`.`date` desc )  AS `rn` from `validation_value` `vv` where (`vv`.`interest` is not null)) `x` where (`x`.`rn` = 1)), `latest_per` as (select `x`.`symbol` AS `symbol`,`x`.`per` AS `per`,`x`.`date` AS `per_date` from (select `q`.`symbol` AS `symbol`,`q`.`per` AS `per`,`q`.`date` AS `date`,row_number() OVER (PARTITION BY `q`.`symbol` ORDER BY `q`.`date` desc )  AS `rn` from `eur_ts_quote` `q` where (`q`.`per` is not null)) `x` where (`x`.`rn` = 1)), `latest_price` as (select `x`.`symbol` AS `symbol`,`x`.`close` AS `close`,`x`.`date` AS `price_date` from (select `q`.`symbol` AS `symbol`,`q`.`close` AS `close`,`q`.`date` AS `date`,row_number() OVER (PARTITION BY `q`.`symbol` ORDER BY `q`.`date` desc )  AS `rn` from `eur_ts_quote` `q` where (`q`.`close` is not null)) `x` where (`x`.`rn` = 1)), `latest_bps` as (select `x`.`symbol` AS `symbol`,`x`.`bps` AS `bps`,`x`.`date` AS `fundamental_date` from (select `f`.`symbol` AS `symbol`,`f`.`bps` AS `bps`,`f`.`date` AS `date`,row_number() OVER (PARTITION BY `f`.`symbol` ORDER BY `f`.`date` desc )  AS `rn` from `eur_fun` `f` where (`f`.`bps` is not null)) `x` where (`x`.`rn` = 1)) select `r`.`symbol` AS `symbol`,`r`.`companyName` AS `company_name`,`i`.`interest` AS `eps_growth`,`i`.`interest_date` AS `interest_date`,`b`.`per_mean` AS `per_mean`,`p`.`per` AS `last_per`,`p`.`per_date` AS `per_date`,(case when ((`b`.`per_mean` > 0) and (`p`.`per` > 0)) then ((pow((`b`.`per_mean` / `p`.`per`),(1.0 / 7.0)) - 1) * 100) else NULL end) AS `per_interest`,`b`.`pbr_mean` AS `pbr_mean`,(`lp`.`close` / nullif(`lb`.`bps`,0)) AS `last_pbr`,`lp`.`price_date` AS `price_date`,`lb`.`fundamental_date` AS `fundamental_date`,(case when ((`b`.`pbr_mean` > 0) and (`lp`.`close` > 0) and (`lb`.`bps` > 0)) then ((pow((`b`.`pbr_mean` / (`lp`.`close` / `lb`.`bps`)),(1.0 / 7.0)) - 1) * 100) else NULL end) AS `pbr_interest`,coalesce((100 / nullif(`b`.`pdr_mean`,0)),0) AS `dividend` from (((((`_reference_map` `r` left join `validation_board` `b` on((`b`.`symbol` = `r`.`symbol`))) left join `latest_interest` `i` on((`i`.`symbol` = `r`.`symbol`))) left join `latest_per` `p` on((`p`.`symbol` = `r`.`symbol`))) left join `latest_price` `lp` on((`lp`.`symbol` = `r`.`symbol`))) left join `latest_bps` `lb` on((`lb`.`symbol` = `r`.`symbol`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `show_all_active_assets_with_last_quote_and_fundamental`
--

/*!50001 DROP VIEW IF EXISTS `show_all_active_assets_with_last_quote_and_fundamental`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `show_all_active_assets_with_last_quote_and_fundamental` AS select `a`.`companyName` AS `companyName`,`a`.`isin` AS `isin`,`c`.`symbol` AS `symbol`,`c`.`max_date` AS `max_date`,`b`.`symbol_fun` AS `symbol_fun`,`b`.`max_date_fun` AS `max_date_fun`,`b`.`max_calendar_year` AS `max_calendar_year` from ((`_reference_map` `a` left join (select `e`.`symbol` AS `symbol_fun`,max(`e`.`date`) AS `max_date_fun`,max(`e`.`calendarYear`) AS `max_calendar_year` from `eur_fun` `e` group by `e`.`symbol`) `b` on((`a`.`symbol_fundamental` = `b`.`symbol_fun`))) left join (select `f`.`symbol` AS `symbol`,max(`f`.`date`) AS `max_date` from `eur_ts_quote` `f` where (`f`.`date` > '2026-01-01') group by `f`.`symbol`) `c` on((`a`.`symbol` = `c`.`symbol`))) where ((`a`.`symbol_fundamental` is not null) and (`a`.`active` = 1)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `validation_value_view`
--

/*!50001 DROP VIEW IF EXISTS `validation_value_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `validation_value_view` AS select `a`.`companyName` AS `companyName`,`b`.`country` AS `country`,`b`.`sector` AS `sector`,`d`.`symbol` AS `symbol`,`d`.`date` AS `date`,`d`.`type` AS `type`,`d`.`rsq` AS `rsq`,`d`.`close` AS `close`,`d`.`sevenYears` AS `sevenYears`,`d`.`fifteenYears` AS `fifteenYears`,`d`.`interest` AS `interest`,`d`.`doubled` AS `doubled`,((2 * `d`.`close`) / nullif((`d`.`sevenYears` + `d`.`fifteenYears`),0)) AS `ratio`,(`d`.`close` / nullif(`c`.`bps`,0)) AS `pbr`,`a`.`pbr_est` AS `pbr_est`,`a`.`per_est` AS `per_est`,`a`.`grossProfitRatio` AS `grossProfitRatio`,`a`.`researchAndDevelopmentRatio` AS `researchAndDevelopmentRatio`,`a`.`interestExpenseRatio` AS `interestExpenseRatio`,`m`.`fairValue_DCF` AS `fairValue_DCF`,`m`.`businessCapitalPreservationStrength` AS `businessCapitalPreservationStrength`,`m`.`shareholderCapitalPreservationStrength` AS `shareholderCapitalPreservationStrength`,`m`.`riskClass` AS `riskClass`,`m`.`date` AS `manualDate`,`d`.`updated` AS `updated` from ((((`validation_board` `a` join `_reference_map` `b` on((`a`.`symbol` = `b`.`symbol`))) join `eps_analyzed` `d` on(((`b`.`symbol` = `d`.`symbol`) and (`d`.`date` = curdate())))) join (select `t`.`symbol` AS `symbol`,`t`.`calendarYear` AS `calendarYear`,`t`.`bps` AS `bps` from (select `eur_fun`.`symbol` AS `symbol`,`eur_fun`.`calendarYear` AS `calendarYear`,`eur_fun`.`bps` AS `bps`,row_number() OVER (PARTITION BY `eur_fun`.`symbol` ORDER BY `eur_fun`.`calendarYear` desc )  AS `rn` from `eur_fun` where ((`eur_fun`.`updated` > (curdate() - interval 1 year)) and (`eur_fun`.`calendarYear` >= (year(curdate()) - 2)))) `t` where (`t`.`rn` = 1)) `c` on((`b`.`symbol_fundamental` = `c`.`symbol`))) left join (select `x`.`symbol` AS `symbol`,`x`.`date` AS `date`,`x`.`fairValue_DCF` AS `fairValue_DCF`,`x`.`businessCapitalPreservationStrength` AS `businessCapitalPreservationStrength`,`x`.`shareholderCapitalPreservationStrength` AS `shareholderCapitalPreservationStrength`,`x`.`riskClass` AS `riskClass`,`x`.`created` AS `created`,`x`.`updated` AS `updated` from (select `validation_manual`.`symbol` AS `symbol`,`validation_manual`.`date` AS `date`,`validation_manual`.`fairValue_DCF` AS `fairValue_DCF`,`validation_manual`.`businessCapitalPreservationStrength` AS `businessCapitalPreservationStrength`,`validation_manual`.`shareholderCapitalPreservationStrength` AS `shareholderCapitalPreservationStrength`,`validation_manual`.`riskClass` AS `riskClass`,`validation_manual`.`created` AS `created`,`validation_manual`.`updated` AS `updated`,row_number() OVER (PARTITION BY `validation_manual`.`symbol` ORDER BY `validation_manual`.`date` desc )  AS `rn` from `validation_manual`) `x` where (`x`.`rn` = 1)) `m` on((`d`.`symbol` = `m`.`symbol`))) where (`b`.`active` = 1) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `validation_value_view_20260527`
--

/*!50001 DROP VIEW IF EXISTS `validation_value_view_20260527`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `validation_value_view_20260527` AS select `a`.`companyName` AS `companyName`,`b`.`country` AS `country`,`b`.`sector` AS `sector`,`d`.`symbol` AS `symbol`,`d`.`date` AS `date`,`d`.`type` AS `type`,`d`.`rsq` AS `rsq`,`d`.`close` AS `close`,`d`.`sevenYears` AS `sevenYears`,`d`.`fifteenYears` AS `fifteenYears`,`d`.`interest` AS `interest`,`d`.`doubled` AS `doubled`,((2 * `d`.`close`) / nullif((`d`.`sevenYears` + `d`.`fifteenYears`),0)) AS `ratio`,(`d`.`close` / nullif(`c`.`bps`,0)) AS `pbr`,`a`.`pbr_est` AS `pbr_est`,`a`.`per_est` AS `per_est`,`a`.`grossProfitRatio` AS `grossProfitRatio`,`a`.`researchAndDevelopmentRatio` AS `researchAndDevelopmentRatio`,`a`.`interestExpenseRatio` AS `interestExpenseRatio`,`d`.`updated` AS `updated` from (((`validation_board` `a` join `_reference_map` `b` on((`a`.`symbol` = `b`.`symbol`))) join `eps_analyzed` `d` on(((`b`.`symbol` = `d`.`symbol`) and (`d`.`date` = curdate())))) join (select `t`.`symbol` AS `symbol`,`t`.`calendarYear` AS `calendarYear`,`t`.`bps` AS `bps` from (select `eur_fun`.`symbol` AS `symbol`,`eur_fun`.`calendarYear` AS `calendarYear`,`eur_fun`.`bps` AS `bps`,row_number() OVER (PARTITION BY `eur_fun`.`symbol` ORDER BY `eur_fun`.`calendarYear` desc )  AS `rn` from `eur_fun` where ((`eur_fun`.`updated` > (curdate() - interval 1 year)) and (`eur_fun`.`calendarYear` >= (year(curdate()) - 2)))) `t` where (`t`.`rn` = 1)) `c` on((`b`.`symbol_fundamental` = `c`.`symbol`))) where (`b`.`active` = 1) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-11  4:26:48
