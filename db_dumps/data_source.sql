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
-- Dumping data for table `data_source`
--

LOCK TABLES `data_source` WRITE;
/*!40000 ALTER TABLE `data_source` DISABLE KEYS */;
INSERT INTO `data_source` VALUES (1,'Yu et al., 2013','http://flybase.org/reports/FBrf0221412.html',NULL,NULL,NULL,'Yu2013',23541733,NULL),(2,'Ito et al., 2013','http://flybase.org/reports/FBrf0221438.html',NULL,NULL,NULL,'Ito2013',23541729,NULL),(3,'Cachero et al., 2010','http://flybase.org/reports/FBrf0211926.html',NULL,NULL,NULL,'Cachero2010',NULL,NULL),(4,'Chiang et al., 2010','http://flybase.org/reports/FBrf0210580.html','http://flycircuit.tw/modules.php?name=clearpage&op=detail_table&idid=',NULL,'FlyCircuit','Chiang2010',21129968,NULL),(5,'Knowles-Barley et al., 2010','http://flybase.org/reports/FBrf0211243.html','http://braintrap.inf.ed.ac.uk/braintrap/line/show?FBti=',NULL,'BrainTrap','Knowles-Barley2010',NULL,NULL),(6,'Jenett et al., 2012','http://flybase.org/reports/FBrf0219813.html','http://flweb.janelia.org/cgi-bin/view_flew_imagery.cgi?line=',NULL,'FlyLight','Jenett2012',23063364,NULL),(7,'Costa and Jefferis et al., IN','unspec','http://flybrain.mrc-lmb.cam.ac.uk/jlabwww/Welcome.html',NULL,'Jefferis lab','CostaJefferis',NULL,NULL);
/*!40000 ALTER TABLE `data_source` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-02-10 22:52:03
