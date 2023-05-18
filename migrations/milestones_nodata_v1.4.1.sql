-- MariaDB dump 10.19  Distrib 10.11.2-MariaDB, for osx10.17 (x86_64)
--
-- Host: localhost    Database: blueboard_milestones
-- ------------------------------------------------------
-- Server version	10.11.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `blueboard_milestones`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `blueboard_milestones` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `blueboard_milestones`;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `client` (
  `uuid` varchar(56) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `time_created` int(11) DEFAULT NULL,
  `time_updated` int(11) DEFAULT NULL,
  `time_ping` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `CNAME` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client_award`
--

DROP TABLE IF EXISTS `client_award`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `client_award` (
  `uuid` varchar(65) NOT NULL,
  `client_uuid` varchar(56) DEFAULT NULL,
  `award_9char` varchar(9) DEFAULT NULL,
  `award_type` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `hero_image` varchar(255) DEFAULT NULL,
  `channel` int(11) DEFAULT NULL,
  `time_created` int(11) DEFAULT NULL,
  `time_updated` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `CACLIENTUUID` (`client_uuid`),
  KEY `CAAWARD9CHAR` (`award_9char`),
  KEY `CAAWARDTYPE` (`award_type`),
  KEY `CACHANNEL` (`channel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client_award`
--

LOCK TABLES `client_award` WRITE;
/*!40000 ALTER TABLE `client_award` DISABLE KEYS */;
/*!40000 ALTER TABLE `client_award` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client_budget`
--

DROP TABLE IF EXISTS `client_budget`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `client_budget` (
  `uuid` varchar(65) NOT NULL,
  `client_uuid` varchar(56) DEFAULT NULL,
  `budget_9char` varchar(9) DEFAULT NULL,
  `parent_9char` varchar(9) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `value` int(11) DEFAULT NULL,
  `time_created` int(11) DEFAULT NULL,
  `time_updated` int(11) DEFAULT NULL,
  `active` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `CBCLIENTUUID` (`client_uuid`),
  KEY `CBBUDGET9CHAR` (`budget_9char`),
  KEY `CBPARENT9CHAR` (`parent_9char`),
  KEY `CBNAME` (`name`),
  KEY `CBACTIVE` (`active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client_budget`
--

LOCK TABLES `client_budget` WRITE;
/*!40000 ALTER TABLE `client_budget` DISABLE KEYS */;
/*!40000 ALTER TABLE `client_budget` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client_user`
--

DROP TABLE IF EXISTS `client_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `client_user` (
  `uuid` varchar(56) NOT NULL,
  `user_uuid` varchar(56) DEFAULT NULL,
  `client_uuid` varchar(56) DEFAULT NULL,
  `manager_uuid` varchar(56) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `department` varchar(255) DEFAULT NULL,
  `employee_id` varchar(255) DEFAULT NULL,
  `active` tinyint(4) DEFAULT NULL,
  `time_created` int(11) DEFAULT NULL,
  `time_updated` int(11) DEFAULT NULL,
  `time_hire` int(11) DEFAULT NULL,
  `time_start` int(11) DEFAULT NULL,
  `admin` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `CUUSERUUID` (`user_uuid`),
  KEY `CUCLIENTUUID` (`client_uuid`),
  KEY `CUMANAGERUUID` (`manager_uuid`),
  KEY `CUDEPARTMENT` (`department`),
  KEY `CUEMPLOYEEID` (`employee_id`),
  KEY `CUTIMEHIRE` (`time_hire`),
  KEY `CUTIMESTART` (`time_start`),
  KEY `CUADMIN` (`admin`),
  KEY `CUACTIVE` (`active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client_user`
--

LOCK TABLES `client_user` WRITE;
/*!40000 ALTER TABLE `client_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `client_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message_template`
--

DROP TABLE IF EXISTS `message_template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `message_template` (
  `uuid` varchar(56) NOT NULL,
  `channel` int(11) DEFAULT NULL,
  `body` longtext DEFAULT NULL,
  `time_created` int(11) DEFAULT NULL,
  `time_updated` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `MTCHANNEL` (`channel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message_template`
--

LOCK TABLES `message_template` WRITE;
/*!40000 ALTER TABLE `message_template` DISABLE KEYS */;
/*!40000 ALTER TABLE `message_template` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program`
--

DROP TABLE IF EXISTS `program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `program` (
  `uuid` varchar(65) NOT NULL,
  `client_uuid` varchar(56) DEFAULT NULL,
  `program_9char` varchar(9) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `budget_9char` varchar(9) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `program_type` int(11) DEFAULT NULL,
  `cadence` int(11) DEFAULT NULL,
  `cadence_value` int(11) DEFAULT NULL,
  `user_uuid` varchar(56) DEFAULT NULL,
  `time_created` int(11) DEFAULT NULL,
  `time_updated` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `PUSERUUID` (`user_uuid`),
  KEY `PPROGRAM9CHAR` (`program_9char`),
  KEY `PCLIENTUUID` (`client_uuid`),
  KEY `PBUDGET9CHAR` (`budget_9char`),
  KEY `PSTATUS` (`status`),
  KEY `PPROGRAMTYPE` (`program_type`),
  KEY `PCADENCE` (`cadence`),
  KEY `PCADENCEVALUE` (`cadence_value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program`
--

LOCK TABLES `program` WRITE;
/*!40000 ALTER TABLE `program` DISABLE KEYS */;
/*!40000 ALTER TABLE `program` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program_admin`
--

DROP TABLE IF EXISTS `program_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `program_admin` (
  `uuid` varchar(56) NOT NULL,
  `program_uuid` varchar(65) DEFAULT NULL,
  `client_uuid` varchar(56) DEFAULT NULL,
  `program_9char` varchar(9) DEFAULT NULL,
  `user_uuid` varchar(56) DEFAULT NULL,
  `permissions` int(11) DEFAULT NULL,
  `time_created` int(11) DEFAULT NULL,
  `time_updated` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `PAPROGRAMUUID` (`program_uuid`),
  KEY `PACLIENTUUID` (`client_uuid`),
  KEY `PAPROGRAM9CHAR` (`program_9char`),
  KEY `PAUSERUUID` (`user_uuid`),
  KEY `PAPERMISSIONS` (`permissions`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program_admin`
--

LOCK TABLES `program_admin` WRITE;
/*!40000 ALTER TABLE `program_admin` DISABLE KEYS */;
/*!40000 ALTER TABLE `program_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program_event`
--

DROP TABLE IF EXISTS `program_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `program_event` (
  `uuid` varchar(72) NOT NULL,
  `program_uuid` varchar(65) DEFAULT NULL,
  `client_uuid` varchar(56) DEFAULT NULL,
  `program_9char` varchar(9) DEFAULT NULL,
  `event_9char` varchar(9) DEFAULT NULL,
  `event_type` int(11) DEFAULT NULL,
  `parent_9char` varchar(9) DEFAULT NULL,
  `segment_9char` varchar(9) DEFAULT NULL,
  `event_data` longtext DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `time_created` int(11) DEFAULT NULL,
  `time_updated` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `PEPROGRAMUUID` (`program_uuid`),
  KEY `PECLIENTUUID` (`client_uuid`),
  KEY `PEPROGRAM9CHAR` (`program_9char`),
  KEY `PEEVENT9CHAR` (`event_9char`),
  KEY `PEEVENTTYPE` (`event_type`),
  KEY `PEPARENT9CHAR` (`parent_9char`),
  KEY `PESEGMENT9CHAR` (`segment_9char`),
  KEY `PESTATUS` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program_event`
--

LOCK TABLES `program_event` WRITE;
/*!40000 ALTER TABLE `program_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `program_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program_message`
--

DROP TABLE IF EXISTS `program_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `program_message` (
  `uuid` varchar(65) NOT NULL,
  `program_uuid` varchar(65) DEFAULT NULL,
  `client_uuid` varchar(56) DEFAULT NULL,
  `program_9char` varchar(9) DEFAULT NULL,
  `message_9char` varchar(9) DEFAULT NULL,
  `template_uuid` varchar(56) DEFAULT NULL,
  `channel` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `time_created` int(11) DEFAULT NULL,
  `time_updated` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `PMPROGRAMUUID` (`program_uuid`),
  KEY `PMCLIENTUUID` (`client_uuid`),
  KEY `PMPROGRAM9CHAR` (`program_9char`),
  KEY `PMMESSAGE9CHAR` (`message_9char`),
  KEY `PMTEMPLATEUUID` (`template_uuid`),
  KEY `PMCHANNEL` (`channel`),
  KEY `PMSTATUS` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program_message`
--

LOCK TABLES `program_message` WRITE;
/*!40000 ALTER TABLE `program_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `program_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program_segment`
--

DROP TABLE IF EXISTS `program_segment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `program_segment` (
  `uuid` varchar(72) NOT NULL,
  `client_uuid` varchar(56) DEFAULT NULL,
  `program_9char` varchar(9) DEFAULT NULL,
  `segment_9char` varchar(9) DEFAULT NULL,
  `budget_9char` varchar(9) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `status` tinyint(4) DEFAULT NULL,
  `time_created` int(11) DEFAULT NULL,
  `time_updated` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `PSCLIENTUUID` (`client_uuid`),
  KEY `PSPROGRAM9CHAR` (`program_9char`),
  KEY `PSSEGMENT9CHAR` (`segment_9char`),
  KEY `PSBUDGET9CHAR` (`budget_9char`),
  KEY `PSSTATUS` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program_segment`
--

LOCK TABLES `program_segment` WRITE;
/*!40000 ALTER TABLE `program_segment` DISABLE KEYS */;
/*!40000 ALTER TABLE `program_segment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program_segment_award`
--

DROP TABLE IF EXISTS `program_segment_award`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `program_segment_award` (
  `uuid` varchar(81) NOT NULL,
  `program_uuid` varchar(65) DEFAULT NULL,
  `client_uuid` varchar(56) DEFAULT NULL,
  `program_9char` varchar(9) DEFAULT NULL,
  `segment_9char` varchar(9) DEFAULT NULL,
  `award_9char` varchar(9) DEFAULT NULL,
  `time_created` int(11) DEFAULT NULL,
  `time_updated` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `PSAPROGRAMUUID` (`program_uuid`),
  KEY `PSACLIENTUUID` (`client_uuid`),
  KEY `PSAPROGRAM9CHAR` (`program_9char`),
  KEY `PSASEGMENT9CHAR` (`segment_9char`),
  KEY `PSAAWARD9char` (`award_9char`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program_segment_award`
--

LOCK TABLES `program_segment_award` WRITE;
/*!40000 ALTER TABLE `program_segment_award` DISABLE KEYS */;
/*!40000 ALTER TABLE `program_segment_award` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program_segment_design`
--

DROP TABLE IF EXISTS `program_segment_design`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `program_segment_design` (
  `uuid` varchar(81) NOT NULL,
  `program_uuid` varchar(65) DEFAULT NULL,
  `client_uuid` varchar(56) DEFAULT NULL,
  `program_9char` varchar(9) DEFAULT NULL,
  `segment_9char` varchar(9) DEFAULT NULL,
  `design_9char` varchar(9) DEFAULT NULL,
  `template_uuid` varchar(56) DEFAULT NULL,
  `channel` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `time_created` int(11) DEFAULT NULL,
  `time_updated` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `PSDPROGRAMUUID` (`program_uuid`),
  KEY `PSDCLIENTUUID` (`client_uuid`),
  KEY `PSDPROGRAM9CHAR` (`program_9char`),
  KEY `PSDSEGMENT9CHAR` (`segment_9char`),
  KEY `PSDDESIGN9CHAR` (`design_9char`),
  KEY `PSDTEMPLATEUUID` (`template_uuid`),
  KEY `PSDCHANNEL` (`channel`),
  KEY `PSDSTATUS` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program_segment_design`
--

LOCK TABLES `program_segment_design` WRITE;
/*!40000 ALTER TABLE `program_segment_design` DISABLE KEYS */;
/*!40000 ALTER TABLE `program_segment_design` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program_segment_rule`
--

DROP TABLE IF EXISTS `program_segment_rule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `program_segment_rule` (
  `uuid` varchar(81) NOT NULL,
  `program_uuid` varchar(65) DEFAULT NULL,
  `client_uuid` varchar(56) DEFAULT NULL,
  `program_9char` varchar(9) DEFAULT NULL,
  `segment_9char` varchar(9) DEFAULT NULL,
  `rule_9char` varchar(9) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `rule_type` int(11) DEFAULT NULL,
  `logic` longtext DEFAULT NULL,
  `time_created` int(11) DEFAULT NULL,
  `time_updated` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `PSRPROGRAMUUID` (`program_uuid`),
  KEY `PSRCLIENTUUID` (`client_uuid`),
  KEY `PSRPROGRAM9CHAR` (`program_9char`),
  KEY `PSRSEGMENT9CHAR` (`segment_9char`),
  KEY `PSRRULE9CHAR` (`rule_9char`),
  KEY `PSRSTATUS` (`status`),
  KEY `PSRRULETYPE` (`rule_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program_segment_rule`
--

LOCK TABLES `program_segment_rule` WRITE;
/*!40000 ALTER TABLE `program_segment_rule` DISABLE KEYS */;
/*!40000 ALTER TABLE `program_segment_rule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `uuid` varchar(56) NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `latitude` int(11) DEFAULT NULL,
  `longitude` int(11) DEFAULT NULL,
  `time_created` int(11) DEFAULT NULL,
  `time_updated` int(11) DEFAULT NULL,
  `time_ping` int(11) DEFAULT NULL,
  `time_birthday` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `UFIRSTNAME` (`first_name`),
  KEY `ULASTNAME` (`last_name`),
  KEY `ULATITUDE` (`latitude`),
  KEY `ULONGITUDE` (`longitude`),
  KEY `UTIMEBIRTHDAY` (`time_birthday`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_service`
--

DROP TABLE IF EXISTS `user_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_service` (
  `uuid` varchar(56) NOT NULL,
  `user_uuid` varchar(56) DEFAULT NULL,
  `service_uuid` varchar(56) DEFAULT NULL,
  `service_user_id` varchar(255) DEFAULT NULL,
  `service_user_screenname` varchar(255) DEFAULT NULL,
  `service_user_name` varchar(255) DEFAULT NULL,
  `service_access_token` varchar(255) DEFAULT NULL,
  `service_access_secret` varchar(255) DEFAULT NULL,
  `service_refresh_token` varchar(255) DEFAULT NULL,
  `time_created` int(11) DEFAULT NULL,
  `time_updated` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `USUSER` (`user_uuid`),
  KEY `USSERVICE` (`service_uuid`),
  KEY `USSERVICEID` (`service_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_service`
--

LOCK TABLES `user_service` WRITE;
/*!40000 ALTER TABLE `user_service` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_service` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-07 18:09:09