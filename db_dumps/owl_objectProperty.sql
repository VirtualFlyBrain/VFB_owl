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
-- Dumping data for table `owl_objectProperty`
--

LOCK TABLES `owl_objectProperty` WRITE;
/*!40000 ALTER TABLE `owl_objectProperty` DISABLE KEYS */;
INSERT INTO `owl_objectProperty` VALUES (21,'RO_0002101','fasciculates_with',2),(46,'RO_0002110','has_postsynaptic_terminal_in',2),(85,'RO_0002131','overlaps',2),(89,'RO_0002202','develops from',2),(92,'BFO_0000050','part_of',2),(97,'RO_0002350','member of',2),(98,'RO_0002351','has member',2),(99,'c099d9d6-4ef3-11e3-9da7-b1ad5291e0b0','exemplar_of',2),(103,'RO_0002292','expresses',2),(104,'0','null_hack',4),(105,'87466F00-CCBA-4632-820E-F619FF3AA087','has_exemplar',2),(106,'depicts',NULL,7),(107,'thumbnail',NULL,7);
/*!40000 ALTER TABLE `owl_objectProperty` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-04-20 23:08:56
