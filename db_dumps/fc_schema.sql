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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `annotation`
--

DROP TABLE IF EXISTS `annotation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `annotation` (
  `annotationid` int(11) NOT NULL AUTO_INCREMENT,
  `user_userid` int(11) NOT NULL,
  `neuron_idid` bigint(20) NOT NULL,
  `annotation_class` varchar(45) NOT NULL,
  `text` varchar(255) NOT NULL,
  `note` text,
  `annotation_uuid` char(36) DEFAULT NULL COMMENT 'db will generate uuids so dont need non-null',
  `created` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`annotationid`),
  UNIQUE KEY `annotation_uuid_UNIQUE` (`annotation_uuid`),
  KEY `fk_annotation_user1` (`user_userid`),
  KEY `fk_annotation_neuron1` (`neuron_idid`),
  KEY `annotation_class` (`annotation_class`),
  CONSTRAINT `fk_annotation_neuron1` FOREIGN KEY (`neuron_idid`) REFERENCES `neuron` (`idid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_annotation_user1` FOREIGN KEY (`user_userid`) REFERENCES `user` (`userid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=24970 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER 
newid
BEFORE INSERT ON 
annotation
FOR EACH ROW
SET NEW.annotation_uuid = UUID() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

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
) ENGINE=MyISAM AUTO_INCREMENT=119 DEFAULT CHARSET=latin1;
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
  `objectProperty` varchar(50) DEFAULT NULL,
  `class` varchar(50) DEFAULT NULL,
  `owl_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `akv` (`annotation_key_value_id`),
  KEY `owl_type_id` (`owl_type_id`),
  CONSTRAINT `annotation_type_ibfk_1` FOREIGN KEY (`owl_type_id`) REFERENCES `owl_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18699 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cluster`
--

DROP TABLE IF EXISTS `cluster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cluster` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cluster` int(11) NOT NULL,
  `clusterv` int(11) NOT NULL,
  `uuid` char(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `cluster_clusterv_UNIQUE` (`cluster`,`clusterv`),
  UNIQUE KEY `uuid_UNIQUE` (`uuid`)
) ENGINE=MyISAM AUTO_INCREMENT=1666 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `flycircuit`.`clusteruuid`
BEFORE INSERT ON `flycircuit`.`cluster`
FOR EACH ROW
SET NEW.uuid = UUID() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `clustering`
--

DROP TABLE IF EXISTS `clustering`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clustering` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idx` bigint(20) DEFAULT NULL,
  `idid` bigint(20) NOT NULL DEFAULT '0',
  `gene_name` text,
  `cluster` bigint(20) DEFAULT NULL,
  `exemplar` text,
  `exemplar_idid` bigint(20) DEFAULT NULL,
  `clusterv_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `idid_plus_version` (`clusterv_id`,`idid`)
) ENGINE=MyISAM AUTO_INCREMENT=48397 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `clusterv`
--

DROP TABLE IF EXISTS `clusterv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clusterv` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clusterobj_name` varchar(128) DEFAULT NULL,
  `clusterobj_hash` varchar(40) NOT NULL,
  `code_hash` varchar(40) NOT NULL,
  `nclusters` int(11) DEFAULT NULL,
  `nitems` int(11) DEFAULT NULL,
  `notes` text,
  `ctime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `uuid` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
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
-- Table structure for table `flycircuit_driver_map`
--

DROP TABLE IF EXISTS `flycircuit_driver_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flycircuit_driver_map` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fc_name` varchar(100) NOT NULL,
  `owl_class_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data_source` int(11) NOT NULL,
  `type` int(11) DEFAULT NULL,
  `baseURI` varchar(100) NOT NULL,
  `URI_end` varchar(100) DEFAULT NULL,
  `is_live` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  UNIQUE KEY `individual_id` (`individual_id`,`type_id`),
  KEY `type_id` (`type_id`),
  CONSTRAINT `individual_type_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `owl_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=240623 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `link`
--

DROP TABLE IF EXISTS `link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `link` (
  `link_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `from_id` bigint(20) NOT NULL,
  `to_id` bigint(20) NOT NULL,
  `link_type` varchar(45) DEFAULT NULL,
  `link_distance` double DEFAULT NULL,
  PRIMARY KEY (`link_id`),
  KEY `fk_link_neuron1` (`from_id`),
  KEY `fk_link_neuron2` (`to_id`),
  KEY `idx_link_type` (`link_type`),
  KEY `idx_link_distance` (`link_distance`),
  CONSTRAINT `fk_link_neuron1` FOREIGN KEY (`from_id`) REFERENCES `neuron` (`idid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_link_neuron2` FOREIGN KEY (`to_id`) REFERENCES `neuron` (`idid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=196614 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lsmxforms`
--

DROP TABLE IF EXISTS `lsmxforms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lsmxforms` (
  `txtfile` varchar(255) DEFAULT NULL,
  `lsmfile` varchar(255) DEFAULT NULL,
  `gene_name` varchar(255) DEFAULT NULL,
  `Ch1` char(6) DEFAULT NULL,
  `Ch2` char(6) DEFAULT NULL,
  `DimensionX` double DEFAULT NULL,
  `DimensionY` double DEFAULT NULL,
  `DimensionZ` double DEFAULT NULL,
  `VoxelSizeX` double DEFAULT NULL,
  `VoxelSizeY` double DEFAULT NULL,
  `VoxelSizeZ` double DEFAULT NULL,
  `noflipcor` tinyint(4) DEFAULT NULL,
  `flipcor` tinyint(4) DEFAULT NULL,
  KEY `gene_name` (`gene_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `neuron`
--

DROP TABLE IF EXISTS `neuron`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `neuron` (
  `gene_name` text,
  `idid` bigint(20) NOT NULL,
  `neuronidurl` text,
  `Name` text,
  `Driver` text,
  `Gender_Age` text,
  `Soma_Coordinate` varchar(128) DEFAULT NULL,
  `Putative_neurotransmitter` text,
  `Putative_birth_time` text,
  `Author` text,
  `Stock` text,
  `Lineage` text,
  `Gender` text,
  `Age` text,
  `Date` text,
  `Soma_X` double DEFAULT NULL,
  `Soma_Y` double DEFAULT NULL,
  `Soma_Z` double DEFAULT NULL,
  `lsmjpgurl` text,
  `lsmjpg300url` text,
  `ziplsmurl` text,
  `lsm` text,
  `ziplsmsize` double DEFAULT NULL,
  `flashurl` text,
  `flashsize` double DEFAULT NULL,
  `download_time` timestamp NULL DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `SpaceCoding` text,
  `uuid` char(36) DEFAULT NULL,
  PRIMARY KEY (`idid`),
  UNIQUE KEY `idid_UNIQUE` (`idid`),
  UNIQUE KEY `uuid_UNIQUE` (`uuid`),
  KEY `Soma_Coordinate_idx` (`Soma_Coordinate`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `flycircuit`.`neuronuuid`
BEFORE INSERT ON `flycircuit`.`neuron`
FOR EACH ROW
SET NEW.uuid = UUID() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Temporary table structure for view `neuronidpages`
--

DROP TABLE IF EXISTS `neuronidpages`;
/*!50001 DROP VIEW IF EXISTS `neuronidpages`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `neuronidpages` (
  `gene_name` tinyint NOT NULL,
  `idid` tinyint NOT NULL,
  `neuronidurl` tinyint NOT NULL,
  `Name` tinyint NOT NULL,
  `Driver` tinyint NOT NULL,
  `Gender_Age` tinyint NOT NULL,
  `Soma_Coordinate` tinyint NOT NULL,
  `Putative_neurotransmitter` tinyint NOT NULL,
  `Putative_birth_time` tinyint NOT NULL,
  `Author` tinyint NOT NULL,
  `Stock` tinyint NOT NULL,
  `Lineage` tinyint NOT NULL,
  `Gender` tinyint NOT NULL,
  `Age` tinyint NOT NULL,
  `Date` tinyint NOT NULL,
  `Soma_X` tinyint NOT NULL,
  `Soma_Y` tinyint NOT NULL,
  `Soma_Z` tinyint NOT NULL,
  `lsmjpgurl` tinyint NOT NULL,
  `lsmjpg300url` tinyint NOT NULL,
  `ziplsmurl` tinyint NOT NULL,
  `lsm` tinyint NOT NULL,
  `ziplsmsize` tinyint NOT NULL,
  `flashurl` tinyint NOT NULL,
  `flashsize` tinyint NOT NULL,
  `download_time` tinyint NOT NULL,
  `last_updated` tinyint NOT NULL,
  `SpaceCoding` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

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
) ENGINE=MyISAM AUTO_INCREMENT=24412 DEFAULT CHARSET=latin1;
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
-- Table structure for table `recipes_new`
--

DROP TABLE IF EXISTS `recipes_new`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recipes_new` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `UUID` varchar(50) DEFAULT NULL,
  `shortFormID` varchar(50) DEFAULT NULL,
  `owl_type` varchar(20) DEFAULT NULL,
  `label` varchar(100) DEFAULT NULL,
  `ontology_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UUID` (`UUID`),
  UNIQUE KEY `shortFormID` (`shortFormID`),
  KEY `ontology_id` (`ontology_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registration`
--

DROP TABLE IF EXISTS `registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registration` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `spatdist_jfrc`
--

DROP TABLE IF EXISTS `spatdist_jfrc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spatdist_jfrc` (
  `idid` double DEFAULT NULL,
  `Exterior` bigint(20) DEFAULT NULL,
  `FB` bigint(20) DEFAULT NULL,
  `EB` bigint(20) DEFAULT NULL,
  `SAD` bigint(20) DEFAULT NULL,
  `NO` bigint(20) DEFAULT NULL,
  `SOG` bigint(20) DEFAULT NULL,
  `PB` bigint(20) DEFAULT NULL,
  `CRE_R` bigint(20) DEFAULT NULL,
  `EPA_R` bigint(20) DEFAULT NULL,
  `VES_R` bigint(20) DEFAULT NULL,
  `ATL_R` bigint(20) DEFAULT NULL,
  `PLP_R` bigint(20) DEFAULT NULL,
  `AVLP_R` bigint(20) DEFAULT NULL,
  `AL_R` bigint(20) DEFAULT NULL,
  `GOR_R` bigint(20) DEFAULT NULL,
  `SCL_R` bigint(20) DEFAULT NULL,
  `FLA` bigint(20) DEFAULT NULL,
  `ICL_R` bigint(20) DEFAULT NULL,
  `ME_R` bigint(20) DEFAULT NULL,
  `LO_R` bigint(20) DEFAULT NULL,
  `MB_R` bigint(20) DEFAULT NULL,
  `PVLP_R` bigint(20) DEFAULT NULL,
  `OTU_R` bigint(20) DEFAULT NULL,
  `WED_R` bigint(20) DEFAULT NULL,
  `SMP_R` bigint(20) DEFAULT NULL,
  `LH_R` bigint(20) DEFAULT NULL,
  `SLP_R` bigint(20) DEFAULT NULL,
  `LB_R` bigint(20) DEFAULT NULL,
  `SIP_R` bigint(20) DEFAULT NULL,
  `IB_R` bigint(20) DEFAULT NULL,
  `IVLP_R` bigint(20) DEFAULT NULL,
  `IPS_R` bigint(20) DEFAULT NULL,
  `SPS_R` bigint(20) DEFAULT NULL,
  `LAL_R` bigint(20) DEFAULT NULL,
  `PRW` bigint(20) DEFAULT NULL,
  `AME_R` bigint(20) DEFAULT NULL,
  `GA_R` bigint(20) DEFAULT NULL,
  `CRE_L` bigint(20) DEFAULT NULL,
  `EPA_L` bigint(20) DEFAULT NULL,
  `VES_L` bigint(20) DEFAULT NULL,
  `ATL_L` bigint(20) DEFAULT NULL,
  `PLP_L` bigint(20) DEFAULT NULL,
  `AVLP_L` bigint(20) DEFAULT NULL,
  `AL_L` bigint(20) DEFAULT NULL,
  `GOR_L` bigint(20) DEFAULT NULL,
  `SCL_L` bigint(20) DEFAULT NULL,
  `ICL_L` bigint(20) DEFAULT NULL,
  `ME_L` bigint(20) DEFAULT NULL,
  `LOP_L` bigint(20) DEFAULT NULL,
  `LO_L` bigint(20) DEFAULT NULL,
  `MB_L` bigint(20) DEFAULT NULL,
  `PVLP_L` bigint(20) DEFAULT NULL,
  `OTU_L` bigint(20) DEFAULT NULL,
  `WED_L` bigint(20) DEFAULT NULL,
  `SMP_L` bigint(20) DEFAULT NULL,
  `LH_L` bigint(20) DEFAULT NULL,
  `SLP_L` bigint(20) DEFAULT NULL,
  `LB_L` bigint(20) DEFAULT NULL,
  `SIP_L` bigint(20) DEFAULT NULL,
  `IB_L` bigint(20) DEFAULT NULL,
  `IVLP_L` bigint(20) DEFAULT NULL,
  `IPS_L` bigint(20) DEFAULT NULL,
  `SPS_L` bigint(20) DEFAULT NULL,
  `LAL_L` bigint(20) DEFAULT NULL,
  `AME_L` bigint(20) DEFAULT NULL,
  `GA_L` bigint(20) DEFAULT NULL,
  `PAN_L` bigint(20) DEFAULT NULL,
  `PAN_R` bigint(20) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `spatialdistribution`
--

DROP TABLE IF EXISTS `spatialdistribution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spatialdistribution` (
  `idid` bigint(20) NOT NULL,
  `rAL` double DEFAULT NULL,
  `lAL` double DEFAULT NULL,
  `rAMMC` double DEFAULT NULL,
  `lAMMC` double DEFAULT NULL,
  `rCAL` double DEFAULT NULL,
  `lCAL` double DEFAULT NULL,
  `rCCP` double DEFAULT NULL,
  `lCCP` double DEFAULT NULL,
  `rCMP` double DEFAULT NULL,
  `lCMP` double DEFAULT NULL,
  `rCVLP` double DEFAULT NULL,
  `lCVLP` double DEFAULT NULL,
  `rDLP` double DEFAULT NULL,
  `lDLP` double DEFAULT NULL,
  `rDMP` double DEFAULT NULL,
  `lDMP` double DEFAULT NULL,
  `rEB` double DEFAULT NULL,
  `lEB` double DEFAULT NULL,
  `rFB` double DEFAULT NULL,
  `lFB` double DEFAULT NULL,
  `rFSPP` double DEFAULT NULL,
  `lFSPP` double DEFAULT NULL,
  `rIDFP` double DEFAULT NULL,
  `lIDFP` double DEFAULT NULL,
  `rIDLP` double DEFAULT NULL,
  `lIDLP` double DEFAULT NULL,
  `rLAT` double DEFAULT NULL,
  `lLAT` double DEFAULT NULL,
  `rLH` double DEFAULT NULL,
  `lLH` double DEFAULT NULL,
  `rLOB` double DEFAULT NULL,
  `lLOB` double DEFAULT NULL,
  `rLOP` double DEFAULT NULL,
  `lLOP` double DEFAULT NULL,
  `rMB` double DEFAULT NULL,
  `lMB` double DEFAULT NULL,
  `rMED` double DEFAULT NULL,
  `lMED` double DEFAULT NULL,
  `rNOD` double DEFAULT NULL,
  `lNOD` double DEFAULT NULL,
  `rOG` double DEFAULT NULL,
  `lOG` double DEFAULT NULL,
  `rOPTU` double DEFAULT NULL,
  `lOPTU` double DEFAULT NULL,
  `rPAN` double DEFAULT NULL,
  `lPAN` double DEFAULT NULL,
  `rPCB` double DEFAULT NULL,
  `lPCB` double DEFAULT NULL,
  `rSDFP` double DEFAULT NULL,
  `lSDFP` double DEFAULT NULL,
  `rSOG` double DEFAULT NULL,
  `lSOG` double DEFAULT NULL,
  `rSPP` double DEFAULT NULL,
  `lSPP` double DEFAULT NULL,
  `rVLP` double DEFAULT NULL,
  `lVLP` double DEFAULT NULL,
  `rVMP` double DEFAULT NULL,
  `lVMP` double DEFAULT NULL,
  PRIMARY KEY (`idid`),
  UNIQUE KEY `idid_UNIQUE` (`idid`),
  KEY `fk_spatialdistribution_neuron` (`idid`),
  CONSTRAINT `fk_spatialdistribution_neuron` FOREIGN KEY (`idid`) REFERENCES `neuron` (`idid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='local annotations for flycuit neurons';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `fullname` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `user_uuid` char(36) NOT NULL,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `user_uuid_UNIQUE` (`user_uuid`),
  UNIQUE KEY `userid_UNIQUE` (`userid`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COMMENT='User for annotation';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ziplsm`
--

DROP TABLE IF EXISTS `ziplsm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ziplsm` (
  `file` text,
  `gene_name` text,
  `zip_size` double DEFAULT NULL,
  `zip_mtime` text,
  `zi_length` double DEFAULT NULL,
  `zi_method` text,
  `zi_size` double DEFAULT NULL,
  `zi_ratio` text,
  `zi_date` text,
  `zi_time` text,
  `zi_crc_32` text,
  `zi_path` text,
  `zi_file` text,
  `zi_gene_name` text,
  `uid` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `neuronidpages`
--

/*!50001 DROP TABLE IF EXISTS `neuronidpages`*/;
/*!50001 DROP VIEW IF EXISTS `neuronidpages`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `neuronidpages` AS select `neuron`.`gene_name` AS `gene_name`,`neuron`.`idid` AS `idid`,`neuron`.`neuronidurl` AS `neuronidurl`,`neuron`.`Name` AS `Name`,`neuron`.`Driver` AS `Driver`,`neuron`.`Gender_Age` AS `Gender_Age`,`neuron`.`Soma_Coordinate` AS `Soma_Coordinate`,`neuron`.`Putative_neurotransmitter` AS `Putative_neurotransmitter`,`neuron`.`Putative_birth_time` AS `Putative_birth_time`,`neuron`.`Author` AS `Author`,`neuron`.`Stock` AS `Stock`,`neuron`.`Lineage` AS `Lineage`,`neuron`.`Gender` AS `Gender`,`neuron`.`Age` AS `Age`,`neuron`.`Date` AS `Date`,`neuron`.`Soma_X` AS `Soma_X`,`neuron`.`Soma_Y` AS `Soma_Y`,`neuron`.`Soma_Z` AS `Soma_Z`,`neuron`.`lsmjpgurl` AS `lsmjpgurl`,`neuron`.`lsmjpg300url` AS `lsmjpg300url`,`neuron`.`ziplsmurl` AS `ziplsmurl`,`neuron`.`lsm` AS `lsm`,`neuron`.`ziplsmsize` AS `ziplsmsize`,`neuron`.`flashurl` AS `flashurl`,`neuron`.`flashsize` AS `flashsize`,`neuron`.`download_time` AS `download_time`,`neuron`.`last_updated` AS `last_updated`,`neuron`.`SpaceCoding` AS `SpaceCoding` from `neuron` */;
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

-- Dump completed on 2014-04-20 15:47:02
