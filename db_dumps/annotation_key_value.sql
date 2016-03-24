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

--
-- Dumping data for table `annotation_key_value`
--

LOCK TABLES `annotation_key_value` WRITE;
/*!40000 ALTER TABLE `annotation_key_value` DISABLE KEYS */;
INSERT INTO `annotation_key_value` VALUES (77,'ALGlomerulus','D doublet'),(70,'ALGlomerulus','DA+'),(44,'ALGlomerulus','DA1'),(90,'ALGlomerulus','DA1+DL3'),(43,'ALGlomerulus','DA2'),(83,'ALGlomerulus','DA4'),(89,'ALGlomerulus','DC2'),(45,'ALGlomerulus','DC3'),(61,'ALGlomerulus','DL1'),(51,'ALGlomerulus','DL2d'),(63,'ALGlomerulus','DL2v'),(87,'ALGlomerulus','DL2v+'),(59,'ALGlomerulus','DL3'),(64,'ALGlomerulus','DL4'),(71,'ALGlomerulus','DM1'),(76,'ALGlomerulus','DM3+'),(69,'ALGlomerulus','DM5'),(53,'ALGlomerulus','DM6'),(46,'ALGlomerulus','DP1l'),(75,'ALGlomerulus','DP1l+'),(73,'ALGlomerulus','DP1m+'),(58,'ALGlomerulus','V'),(66,'ALGlomerulus','V+'),(42,'ALGlomerulus','VA1d'),(56,'ALGlomerulus','VA1lm'),(88,'ALGlomerulus','VA1lm+'),(57,'ALGlomerulus','VA4'),(48,'ALGlomerulus','VA7m'),(85,'ALGlomerulus','VC2'),(55,'ALGlomerulus','VC3+'),(67,'ALGlomerulus','VC3l'),(68,'ALGlomerulus','VC3m'),(84,'ALGlomerulus','VC4?'),(86,'ALGlomerulus','VL2a'),(50,'ALGlomerulus','VL2p'),(52,'ALGlomerulus','VM1'),(74,'ALGlomerulus','VM2'),(82,'ALGlomerulus','VM3'),(62,'ALGlomerulus','VM4'),(65,'ALGlomerulus','VM4+'),(72,'ALGlomerulus','VM4+?'),(49,'ALGlomerulus','VM5d'),(54,'ALGlomerulus','VM5v'),(81,'ALGlomerulus','VM6+'),(78,'ALGlomerulus','VM6+VP1'),(60,'ALGlomerulus','VM7'),(80,'ALGlomerulus','VP1?'),(47,'ALGlomerulus','VP3'),(79,'ALGlomerulus','VP3?'),(4,'Cell Body','Displaced'),(111,'fcerror','image'),(9,'fcerror','segmentation'),(10,'fcerror','warping'),(112,'frunb','aSP-i'),(2,'ImageType','Almost Whole Brain'),(3,'ImageType','Half Brain'),(1,'ImageType','Whole Brain'),(8,'jfcerror','cell body'),(108,'jfcerror','confocal_imaging'),(106,'jfcerror','duplicate_web_image'),(102,'jfcerror','lsm error'),(12,'jfcerror','lsm-web-image-mismatch'),(11,'jfcerror','nrrdcrcdup'),(98,'jfcerror','registration'),(24,'jfcerror','segmentation'),(19,'jfcerror','warping'),(107,'jfcerror','web-segmented-mismatch'),(14,'laterality','cb_mismatch'),(6,'laterality','farcontra'),(7,'laterality','nearcontra'),(22,'laterality','proj_bilat_asymm'),(21,'laterality','proj_bilat_symm'),(20,'laterality','proj_left'),(23,'laterality','proj_midline'),(18,'laterality','proj_right'),(97,'laterality','recheck'),(16,'laterality','soma_left'),(15,'laterality','soma_midline'),(17,'laterality','soma_right'),(34,'MainTract','iACT'),(37,'MainTract','mACT'),(36,'MainTract','oACT'),(40,'MainTract','omACT'),(38,'MainTract','other'),(39,'MainTract','posterior to mACT'),(41,'MainTract','t1ALT'),(114,'MainTract','t2ALT'),(35,'MainTract','t3ALT'),(93,'NeuronSubType','oligoPN'),(91,'NeuronSubType','polyglomerularPN'),(92,'NeuronSubType','uPN'),(115,'NeuronSubType','ventroposterior AL'),(26,'NeuronType','adPN'),(33,'NeuronType','AL Descending Neuron'),(28,'NeuronType','bilateral PN'),(31,'NeuronType','contra adPN'),(30,'NeuronType','contra PN'),(5,'NeuronType','ContraProjAcrossALs'),(113,'NeuronType','descending neuron'),(25,'NeuronType','lPN'),(29,'NeuronType','lPN?'),(32,'NeuronType','vlPN'),(27,'NeuronType','vPN'),(100,'process','flipstack'),(99,'process','note'),(104,'process','segmented_channel'),(105,'process','segmented_image'),(101,'process','swapchannels'),(96,'process','v2good'),(109,'process','v3bad'),(110,'process','v3OK'),(94,'processerror','bad_affine'),(95,'processerror','bad_ght'),(13,'processerror','cb_mismatch'),(117,'processerror','laterality'),(103,'processerror','missing_image'),(118,'processerror','v3toflip');
/*!40000 ALTER TABLE `annotation_key_value` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-04-20 23:11:25
