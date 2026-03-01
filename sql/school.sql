-- MySQL dump 10.13  Distrib 8.0.45, for macos14.8 (arm64)
--
-- Host: 127.0.0.1    Database: student
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `grades`
--

DROP TABLE IF EXISTS `grades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `student_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subject` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `score` decimal(5,2) NOT NULL,
  `exam_date` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `semester` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grades`
--

LOCK TABLES `grades` WRITE;
/*!40000 ALTER TABLE `grades` DISABLE KEYS */;
INSERT INTO `grades` VALUES (1,1,'huyouqiang','数学',80.00,'2024-12-05','2024-05-20'),(2,2,'阿斯蒂芬撒旦法','数学',99.00,'2024-12-05','2024-05-20'),(3,6,'阿达发达','数学',100.00,'2024-12-05','2024-05-20'),(4,20,'hu-.20','数学',100.00,'2024-12-05','2024-05-20'),(5,5,'二哥','数学',100.00,'2024-12-05','2024-05-20');
/*!40000 ALTER TABLE `grades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schools`
--

DROP TABLE IF EXISTS `schools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schools` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `school_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `student_count` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schools`
--

LOCK TABLES `schools` WRITE;
/*!40000 ALTER TABLE `schools` DISABLE KEYS */;
INSERT INTO `schools` VALUES (1,'上海一中','徐汇区','高中',10);
/*!40000 ALTER TABLE `schools` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `age` int NOT NULL,
  `grade` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'huyouqiang',20,'高一'),(2,'阿斯蒂芬撒旦法',10,'收发文呃呃发'),(3,'萨法',55,'撒的方法'),(4,'水电费撒旦法',66,'啊发斯蒂芬是的'),(5,'二哥',99,'阿是发顺丰'),(6,'阿达发达',66,'萨顶顶萨芬'),(8,'hu-.8',8,'班级-8'),(9,'hu-.9',9,'班级-9'),(10,'hu-.10',10,'班级-10'),(11,'hu-.11',11,'班级-11'),(12,'hu-.12',12,'班级-12'),(13,'hu-.13',13,'班级-13'),(14,'hu-.14',14,'班级-14'),(15,'hu-.15',15,'班级-15'),(16,'hu-.16',16,'班级-16'),(17,'hu-.17',17,'班级-17'),(18,'hu-.18',18,'班级-18'),(19,'hu-.19',19,'班级-19'),(20,'hu-.20',20,'班级-20'),(21,'hu-.21',21,'班级-21'),(22,'hu-.22',22,'班级-22'),(23,'hu-.23',23,'班级-23'),(24,'hu-.24',24,'班级-24'),(25,'hu-.25',25,'班级-25'),(26,'hu-.26',26,'班级-26'),(27,'hu-.27',27,'班级-27'),(28,'hu-.28',28,'班级-28'),(29,'hu-.29',29,'班级-29'),(30,'hu-.30',30,'班级-30'),(31,'hu-.31',31,'班级-31'),(32,'hu-.32',32,'班级-32'),(33,'hu-.33',33,'班级-33'),(34,'hu-.34',34,'班级-34'),(35,'hu-.35',35,'班级-35'),(36,'hu-.36',36,'班级-36'),(37,'hu-.37',37,'班级-37'),(38,'hu-.38',38,'班级-38'),(39,'hu-.39',39,'班级-39'),(40,'hu-.40',40,'班级-40'),(41,'hu-.41',41,'班级-41'),(42,'hu-.42',42,'班级-42'),(43,'hu-.43',43,'班级-43'),(44,'hu-.44',44,'班级-44'),(45,'hu-.45',45,'班级-45'),(46,'hu-.46',46,'班级-46'),(47,'hu-.47',47,'班级-47'),(48,'hu-.48',48,'班级-48'),(49,'hu-.49',49,'班级-49'),(50,'hu-.50',50,'班级-50'),(51,'hu-.51',51,'班级-51'),(52,'hu-.52',52,'班级-52'),(53,'hu-.53',53,'班级-53'),(54,'hu-.54',54,'班级-54'),(55,'hu-.55',55,'班级-55'),(56,'hu-.56',56,'班级-56'),(57,'hu-.57',57,'班级-57'),(58,'hu-.58',58,'班级-58'),(59,'hu-.59',59,'班级-59'),(60,'hu-.60',60,'班级-60'),(61,'hu-.61',61,'班级-61'),(62,'hu-.62',62,'班级-62'),(63,'hu-.63',63,'班级-63'),(64,'hu-.64',64,'班级-64'),(65,'hu-.65',65,'班级-65'),(66,'hu-.66',66,'班级-66'),(67,'hu-.67',67,'班级-67'),(68,'hu-.68',68,'班级-68'),(69,'hu-.69',69,'班级-69'),(70,'hu-.70',70,'班级-70'),(71,'hu-.71',71,'班级-71'),(72,'hu-.72',72,'班级-72'),(73,'hu-.73',73,'班级-73'),(74,'hu-.74',74,'班级-74'),(75,'hu-.75',75,'班级-75'),(76,'hu-.76',76,'班级-76'),(77,'hu-.77',77,'班级-77'),(78,'hu-.78',78,'班级-78'),(79,'hu-.79',79,'班级-79'),(80,'hu-.80',80,'班级-80'),(81,'hu-.81',81,'班级-81'),(82,'hu-.82',82,'班级-82'),(83,'hu-.83',83,'班级-83'),(84,'hu-.84',84,'班级-84'),(85,'hu-.85',85,'班级-85'),(86,'hu-.86',86,'班级-86'),(87,'hu-.87',87,'班级-87'),(88,'hu-.88',88,'班级-88'),(89,'hu-.89',89,'班级-89'),(90,'hu-.90',90,'班级-90'),(91,'hu-.91',91,'班级-91'),(92,'hu-.92',92,'班级-92'),(93,'hu-.93',93,'班级-93'),(94,'hu-.94',94,'班级-94'),(95,'hu-.95',95,'班级-95'),(96,'hu-.96',96,'班级-96'),(97,'hu-.97',97,'班级-97'),(98,'hu-.98',98,'班级-98'),(99,'hu-.99',99,'班级-99'),(100,'hu-.100',100,'班级-100');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subject` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `title` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` VALUES (1,'王老师','数学','高级教师','173 2232 1147');
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pass` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` tinyint NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','e75f412fd3260fb4dcf9fc139dbeb566f5781e679b84b42b2afd3e3aba124735',0),(2,'hu','b5eb8fd7c03c97b9d45d03f275e5db669991d602700f5876067585dbe55e3542',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-01 18:08:42
