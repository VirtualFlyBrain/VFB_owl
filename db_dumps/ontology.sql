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
-- Dumping data for table `ontology`
--

LOCK TABLES `ontology` WRITE;
/*!40000 ALTER TABLE `ontology` DISABLE KEYS */;
INSERT INTO `ontology` VALUES (1,'fbbt-simple.owl','http://purl.obolibrary.org/obo/fbbt/fbbt-simple.owl','http://purl.obolibrary.org/obo/','fbbt'),(2,'ro.owl','http://purl.obolibrary.org/obo/ro.owl','http://purl.obolibrary.org/obo/','ro'),(3,'fb_features.owl','http://purl.obolibrary.org/fbbt/fbfeat/fb_features.owl','http://flybase.org/reports/','fb_feat'),(4,'null_hack','null_hack','null_hack',NULL),(5,'flycircuit_plus.owl','http://purl.obolibrary.org/obo/vfb/flycircuit_plus.owl','http://purl.obolibrary.org/obo/vfb/',NULL),(6,'so.owl','http://purl.obolibrary.org/obo/so/so.owl','http://purl.obolibrary.org/obo/','so'),(7,'20140114.rdf','http://xmlns.com/foaf/spec/20140114.rdf','http://xmlns.com/foaf/0.1/','foaf'),(8,'vfb_ext.owl','http://purl.obolibrary.org/obo/vfb/vfb_ext.owl','http://purl.obolibrary.org/obo/vfb/','vfb_ext'),(9,'vfb_ind.owl','http://purl.obolibrary.org/obo/vfb/vfb_ind.owl','http://www.virtualflybrain.org/owl/','vfb_ind');
/*!40000 ALTER TABLE `ontology` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-04-20 23:10:09
