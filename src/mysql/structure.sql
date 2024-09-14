-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: fmp
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
  `longTimeSerie` tinyint NOT NULL DEFAULT '1',
  `comment` text,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`symbol`),
  UNIQUE KEY `symbol_UNIQUE` (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='reference for all the time-series quotes and fundamentals to be queried and merged';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eur_overview`
--

DROP TABLE IF EXISTS `eur_overview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eur_overview` (
  `symbol` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `price_eur` double GENERATED ALWAYS AS ((`price` / `fx_close`)) VIRTUAL,
  `min_eur` double GENERATED ALWAYS AS ((`min` / `fx_close`)) VIRTUAL,
  `max_eur` double GENERATED ALWAYS AS ((`max` / `fx_close`)) VIRTUAL,
  `lastDiv_eur` double GENERATED ALWAYS AS ((`lastDiv` / `fx_close`)) VIRTUAL,
  `mktCap_eur` bigint GENERATED ALWAYS AS ((`mktCap` / `fx_close`)) VIRTUAL,
  `companyName` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `currency` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `isin` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `exchangeShortName` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `industry` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `sector` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `country` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `updated` datetime DEFAULT NULL,
  `price` double DEFAULT NULL,
  `min` double DEFAULT NULL,
  `max` double DEFAULT NULL,
  `range` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `lastDiv` double DEFAULT NULL,
  `mktCap` bigint DEFAULT NULL,
  `fx_close` double DEFAULT NULL,
  PRIMARY KEY (`symbol`),
  UNIQUE KEY `symbol_UNIQUE` (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `eps` double GENERATED ALWAYS AS (if((`per` is not null),(`close` / `per`),NULL)) STORED,
  `per` double DEFAULT NULL,
  `currency` varchar(3) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`date`,`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='QUOTE: data (in EUR) from raw_ts_quote and eur_ts_fx';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-14 20:25:35
