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
  `owl_mapping` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `annotation_class_text_unique` (`annotation_class`,`annotation_text`)
) ENGINE=MyISAM AUTO_INCREMENT=119 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `annotation_key_value`
--

LOCK TABLES `annotation_key_value` WRITE;
/*!40000 ALTER TABLE `annotation_key_value` DISABLE KEYS */;
INSERT INTO `annotation_key_value` VALUES (1,'ImageType','Whole Brain',NULL),(2,'ImageType','Almost Whole Brain',NULL),(3,'ImageType','Half Brain',NULL),(4,'Cell Body','Displaced',NULL),(5,'NeuronType','ContraProjAcrossALs',NULL),(6,'laterality','farcontra',NULL),(7,'laterality','nearcontra',NULL),(8,'jfcerror','cell body',NULL),(9,'fcerror','segmentation',NULL),(10,'fcerror','warping',NULL),(11,'jfcerror','nrrdcrcdup',NULL),(12,'jfcerror','lsm-web-image-mismatch',NULL),(13,'processerror','cb_mismatch',NULL),(14,'laterality','cb_mismatch',NULL),(15,'laterality','soma_midline',NULL),(16,'laterality','soma_left',NULL),(17,'laterality','soma_right',NULL),(18,'laterality','proj_right',NULL),(19,'jfcerror','warping',NULL),(20,'laterality','proj_left',NULL),(21,'laterality','proj_bilat_symm',NULL),(22,'laterality','proj_bilat_asymm',NULL),(23,'laterality','proj_midline',NULL),(24,'jfcerror','segmentation',NULL),(25,'NeuronType','lPN','RO_0002202 some FBbt_00067347'),(26,'NeuronType','adPN','RO_0002202 some FBbt_00067346'),(27,'NeuronType','vPN','RO_0002202 some FBbt_00067348'),(28,'NeuronType','bilateral PN',NULL),(29,'NeuronType','lPN?',NULL),(30,'NeuronType','contra PN',NULL),(31,'NeuronType','contra adPN','RO_0002202 some FBbt_00067346'),(32,'NeuronType','vlPN',NULL),(33,'NeuronType','AL Descending Neuron',NULL),(34,'MainTract','iACT','RO_0002101 some FBbt_00003985'),(35,'MainTract','t3ALT',NULL),(36,'MainTract','oACT',NULL),(37,'MainTract','mACT','RO_0002101 some FBbt_00003984'),(38,'MainTract','other',NULL),(39,'MainTract','posterior to mACT',NULL),(40,'MainTract','omACT','RO_0002101 some FBbt_00007482'),(41,'MainTract','t1ALT',NULL),(42,'ALGlomerulus','VA1d','RO_0002110 some FBbt_00007101'),(43,'ALGlomerulus','DA2',NULL),(44,'ALGlomerulus','DA1','RO_0002110 some FBbt_00003932'),(45,'ALGlomerulus','DC3','RO_0002110 some FBbt_00003963'),(46,'ALGlomerulus','DP1l','RO_0002110 some FBbt_00007098'),(47,'ALGlomerulus','VP3',NULL),(48,'ALGlomerulus','VA7m','RO_0002110 some FBbt_00007102'),(49,'ALGlomerulus','VM5d','RO_0002110 some FBbt_00007391'),(50,'ALGlomerulus','VL2p','RO_0002110 some FBbt_00007107'),(51,'ALGlomerulus','DL2d','RO_0002110 some FBbt_00100377'),(52,'ALGlomerulus','VM1','RO_0002110 some FBbt_00003956'),(53,'ALGlomerulus','DM6','RO_0002110 some FBbt_00003941'),(54,'ALGlomerulus','VM5v','RO_0002110 some FBbt_00007365'),(55,'ALGlomerulus','VC3+',NULL),(56,'ALGlomerulus','VA1lm',NULL),(57,'ALGlomerulus','VA4','RO_0002110 some FBbt_00003944'),(58,'ALGlomerulus','V','RO_0002110 some FBbt_00003951'),(59,'ALGlomerulus','DL3','RO_0002110 some FBbt_00003964'),(60,'ALGlomerulus','VM7','RO_0002110 some FBbt_00003973'),(61,'ALGlomerulus','DL1','RO_0002110 some FBbt_00003968'),(62,'ALGlomerulus','VM4','RO_0002110 some FBbt_00003947'),(63,'ALGlomerulus','DL2v','RO_0002110 some FBbt_00100376'),(64,'ALGlomerulus','DL4','RO_0002110 some FBbt_00003965'),(65,'ALGlomerulus','VM4+','RO_0002110 some FBbt_00003947'),(66,'ALGlomerulus','V+','RO_0002110 some FBbt_00003951'),(67,'ALGlomerulus','VC3l',NULL),(68,'ALGlomerulus','VC3m',NULL),(69,'ALGlomerulus','DM5','RO_0002110 some FBbt_00003940'),(70,'ALGlomerulus','DA+',NULL),(71,'ALGlomerulus','DM1','RO_0002110 some FBbt_00003975'),(72,'ALGlomerulus','VM4+?',NULL),(73,'ALGlomerulus','DP1m+',NULL),(74,'ALGlomerulus','VM2','RO_0002110 some FBbt_00003947'),(75,'ALGlomerulus','DP1l+','RO_0002110 some FBbt_00007098'),(76,'ALGlomerulus','DM3+','RO_0002110 some FBbt_00003972'),(77,'ALGlomerulus','D doublet',NULL),(78,'ALGlomerulus','VM6+VP1',NULL),(79,'ALGlomerulus','VP3?',NULL),(80,'ALGlomerulus','VP1?',NULL),(81,'ALGlomerulus','VM6+',NULL),(82,'ALGlomerulus','VM3',NULL),(83,'ALGlomerulus','DA4',NULL),(84,'ALGlomerulus','VC4?',NULL),(85,'ALGlomerulus','VC2',NULL),(86,'ALGlomerulus','VL2a','RO_0002110 some FBbt_00007106'),(87,'ALGlomerulus','DL2v+','RO_0002110 some FBbt_00100376'),(88,'ALGlomerulus','VA1lm+',NULL),(89,'ALGlomerulus','DC2',NULL),(90,'ALGlomerulus','DA1+DL3',NULL),(91,'NeuronSubType','polyglomerularPN',NULL),(92,'NeuronSubType','uPN','FBbt_00007383'),(93,'NeuronSubType','oligoPN','FBbt_00007384'),(94,'processerror','bad_affine',NULL),(95,'processerror','bad_ght',NULL),(96,'process','v2good',NULL),(97,'laterality','recheck',NULL),(98,'jfcerror','registration',NULL),(99,'process','note',NULL),(100,'process','flipstack',NULL),(101,'process','swapchannels',NULL),(102,'jfcerror','lsm error',NULL),(103,'processerror','missing_image',NULL),(104,'process','segmented_channel',NULL),(105,'process','segmented_image',NULL),(106,'jfcerror','duplicate_web_image',NULL),(107,'jfcerror','web-segmented-mismatch',NULL),(108,'jfcerror','confocal_imaging',NULL),(109,'process','v3bad',NULL),(110,'process','v3OK',NULL),(111,'fcerror','image',NULL),(112,'frunb','aSP-i',NULL),(113,'NeuronType','descending neuron',NULL),(114,'MainTract','t2ALT',NULL),(115,'NeuronSubType','ventroposterior AL',NULL),(117,'processerror','laterality',NULL),(118,'processerror','v3toflip',NULL);
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

-- Dump completed on 2014-02-10 22:49:27
