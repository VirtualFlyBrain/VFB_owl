-- MySQL dump 10.13  Distrib 5.6.14, for osx10.7 (x86_64)
--
-- Host: localhost    Database: flycircuit
-- ------------------------------------------------------
-- Server version	5.6.14

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `owl_class`
--

DROP TABLE IF EXISTS `owl_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `owl_class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shortFormID` varchar(50) DEFAULT NULL,
  `label` varchar(100) DEFAULT NULL,
  `ontology_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `shortFormID` (`shortFormID`),
  KEY `ontology_id` (`ontology_id`),
  CONSTRAINT `owl_class_ibfk_1` FOREIGN KEY (`ontology_id`) REFERENCES `ontology` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4852 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `owl_objectProperty`
--

DROP TABLE IF EXISTS `owl_objectProperty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `owl_objectProperty` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shortFormID` varchar(50) DEFAULT NULL,
  `label` varchar(100) DEFAULT NULL,
  `ontology_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `shortFormID` (`shortFormID`),
  KEY `ontology_id` (`ontology_id`),
  CONSTRAINT `owl_objectproperty_ibfk_1` FOREIGN KEY (`ontology_id`) REFERENCES `ontology` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `owl_individual`
--

DROP TABLE IF EXISTS `owl_individual`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `owl_individual` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shortFormID` varchar(12) DEFAULT NULL,
  `uuid` char(36) NOT NULL,
  `type_for_def` varchar(45) DEFAULT NULL,
  `source_id` int(11) NOT NULL,
  `label` varchar(50) DEFAULT NULL,
  `is_obsolete` binary(1) NOT NULL DEFAULT '0',
  `ID_in_source` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid_UNIQUE` (`uuid`),
  UNIQUE KEY `vfbid` (`shortFormID`),
  UNIQUE KEY `vfbid_UNIQUE` (`shortFormID`),
  UNIQUE KEY `vfbid_2` (`shortFormID`),
  KEY `source` (`source_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24412 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `owl_type`
--

DROP TABLE IF EXISTS `owl_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `owl_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `objectProperty` int(11) DEFAULT NULL,
  `class` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `utype` (`class`,`objectProperty`),
  KEY `objectProperty` (`objectProperty`),
  CONSTRAINT `owl_type_ibfk_1` FOREIGN KEY (`class`) REFERENCES `owl_class` (`id`),
  CONSTRAINT `owl_type_ibfk_2` FOREIGN KEY (`objectProperty`) REFERENCES `owl_objectProperty` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8416 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `individual_type`
--

DROP TABLE IF EXISTS `individual_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `individual_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `individual_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  `for_text_def` binary(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  KEY `itfk` (`individual_id`),
  CONSTRAINT `itfk` FOREIGN KEY (`individual_id`) REFERENCES `owl_individual` (`id`),
  CONSTRAINT `individual_type_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `owl_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=240623 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `BrainName_to_owl`
--

DROP TABLE IF EXISTS `BrainName_to_owl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BrainName_to_owl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `BrainName_abbv` varchar(12) NOT NULL,
  `owl_class_id` int(11) DEFAULT NULL,
  `stack_index` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `claz` (`owl_class_id`),
  CONSTRAINT `claz` FOREIGN KEY (`owl_class_id`) REFERENCES `owl_class` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `annotation_type`
--

DROP TABLE IF EXISTS `annotation_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `annotation_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `annotation_key_value_id` int(11) NOT NULL,
  `owl_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `owl_type_id` (`owl_type_id`),
  KEY `akv` (`annotation_key_value_id`),
  CONSTRAINT `akv` FOREIGN KEY (`annotation_key_value_id`) REFERENCES `annotation_key_value` (`id`),
  CONSTRAINT `annotation_type_ibfk_1` FOREIGN KEY (`owl_type_id`) REFERENCES `owl_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18699 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_source`
--

DROP TABLE IF EXISTS `data_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pub_miniref` char(30) NOT NULL,
  `dataset_link` text NOT NULL,
  `data_link_pre` text,
  `data_link_post` text,
  `data_link_display_name` text,
  `name` char(30) NOT NULL,
  `pub_pmid` int(11) DEFAULT NULL,
  `dataset_spec_text` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dataset_display_name` (`pub_miniref`),
  UNIQUE KEY `dataset_display_name_2` (`pub_miniref`),
  UNIQUE KEY `dataset_short_display_name` (`name`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `pub_miniref` (`pub_miniref`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ontology`
--

DROP TABLE IF EXISTS `ontology`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ontology` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(50) DEFAULT NULL,
  `URI` varchar(100) NOT NULL,
  `baseURI` varchar(100) NOT NULL,
  `short_name` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `URI` (`URI`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `annotation_key_value`
--

DROP TABLE IF EXISTS `annotation_key_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `annotation_key_value` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `annotation_class` varchar(45) NOT NULL,
  `annotation_text` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `annotation_class_text_unique` (`annotation_class`,`annotation_text`)
) ENGINE=InnoDB AUTO_INCREMENT=119 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-04-20 17:15:30
