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
-- Dumping data for table `annotation_type`
--

LOCK TABLES `annotation_type` WRITE;
/*!40000 ALTER TABLE `annotation_type` DISABLE KEYS */;
INSERT INTO `annotation_type` VALUES (18662,25,'89','88',8205),(18663,26,'89','87',8206),(18664,27,'89','86',8207),(18665,31,'89','87',8206),(18666,34,'21','19',8208),(18667,37,'21','20',8209),(18668,40,'21','18',8210),(18669,42,'46','37',8211),(18670,44,'46','35',8212),(18671,45,'46','40',8213),(18672,46,'46','30',8214),(18673,48,'46','41',8215),(18674,49,'46','32',8216),(18675,50,'46','23',8217),(18676,51,'46','39',8218),(18677,52,'46','22',8219),(18678,53,'46','29',8220),(18679,54,'46','45',8221),(18680,57,'46','33',8222),(18681,58,'46','28',8223),(18682,59,'46','38',8224),(18683,60,'46','26',8225),(18684,61,'46','43',8226),(18685,62,'46','27',8227),(18686,63,'46','31',8228),(18687,64,'46','44',8229),(18688,65,'46','27',8227),(18689,66,'46','28',8223),(18690,69,'46','25',8230),(18691,71,'46','34',8231),(18692,74,'46','27',8227),(18693,75,'46','30',8214),(18694,76,'46','24',8232),(18695,86,'46','42',8233),(18696,87,'46','31',8228),(18697,92,'104','94',8234),(18698,93,'104','93',8235);
/*!40000 ALTER TABLE `annotation_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-02-17 18:59:34
