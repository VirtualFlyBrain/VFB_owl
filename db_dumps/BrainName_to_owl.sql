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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `BrainName_to_owl`
--

LOCK TABLES `BrainName_to_owl` WRITE;
/*!40000 ALTER TABLE `BrainName_to_owl` DISABLE KEYS */;
INSERT INTO `BrainName_to_owl` VALUES (1,'MB_R',47),(2,'CRE_L',48),(3,'SPS_R',49),(4,'PVLP_L',50),(5,'MB_L',47),(6,'IVLP_R',51),(7,'PLP_R',52),(8,'AME_L',53),(9,'ICL_R',54),(10,'LH_L',55),(11,'LO_L',56),(12,'SOG',57),(13,'EPA_R',58),(14,'PAN_L',59),(15,'AL_R',60),(16,'AVLP_R',61),(17,'LB_L',62),(18,'SPS_L',49),(19,'SLP_L',63),(20,'GOR_L',64),(21,'ATL_L',65),(22,'OTU_L',66),(23,'GA_L',67),(24,'WED_L',68),(25,'VES_L',69),(26,'IB_L',70),(27,'NO',71),(28,'AVLP_L',61),(29,'LH_R',55),(30,'IPS_R',72),(31,'PAN_R',59),(32,'PB',73),(33,'IPS_L',72),(34,'ME_L',74),(35,'VES_R',69),(36,'LB_R',62),(37,'SIP_L',75),(38,'FLA',76),(39,'PVLP_R',50),(40,'LAL_R',77),(41,'SMP_R',78),(42,'FB',79),(43,'SMP_L',78),(44,'SAD',80),(45,'IB_R',70),(46,'SIP_R',75),(47,'EPA_L',58),(48,'GA_R',67),(49,'WED_R',68),(50,'AME_R',53),(51,'ATL_R',65),(52,'ME_R',74),(53,'LO_R',56),(54,'LOP_L',81),(55,'EB',82),(56,'SCL_L',83),(57,'OTU_R',66),(58,'CRE_R',48),(59,'IVLP_L',51),(60,'AL_L',60),(61,'LAL_L',77),(62,'PRW',84),(63,'PLP_L',52),(64,'SLP_R',63),(65,'SCL_R',83),(66,'GOR_R',64),(67,'ICL_L',54);
/*!40000 ALTER TABLE `BrainName_to_owl` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-02-17 19:10:19
