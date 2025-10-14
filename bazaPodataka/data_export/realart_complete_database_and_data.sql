CREATE DATABASE  IF NOT EXISTS `realart` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `realart`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: realart
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$DfTurEcpgib1U4gTheaKSh$kNHoTuWe/xIy5R+wu/1LnMG4zqDPsr+yQBUIpwr268o=','2025-10-13 22:59:47.322110',0,'minnie','','','',0,1,'2025-10-11 13:54:07.695107'),(2,'pbkdf2_sha256$1000000$NYdswgOhqDPrComMq9xKRV$AANZ94Yb2d8UPYuAN/FbgUAxanSGVtFommYeCrurCAQ=','2025-10-12 13:22:45.480727',0,'stole','','','',0,1,'2025-10-11 13:58:16.968988'),(3,'pbkdf2_sha256$1000000$QAe5xrkGPp9gOuSJ5h0hm5$fJL2XUv8BbK42VEyg4F/0WAx2x1fpw2b2tBf0yPmU4U=','2025-10-13 23:13:36.972338',0,'marko2003','','','',0,1,'2025-10-11 14:02:05.864076'),(4,'pbkdf2_sha256$1000000$jhye9W6paxTxYP9kGL0KOm$qPiiUMaeUTXTGmEAlLrQiWBszGql+wTAIXvKYe3Gj4Q=','2025-10-13 22:47:03.778876',0,'iloveart','','','',0,1,'2025-10-11 14:03:32.895488'),(5,'pbkdf2_sha256$1000000$VXVu7wzkd05zAPqNn4H1z7$EoS69nWNPUuEiqLdL4S0p2bRqq8RvMmmx+zu/HOs5vE=','2025-10-12 17:50:36.994388',0,'reks','','','',0,1,'2025-10-11 14:05:10.935807'),(6,'pbkdf2_sha256$1000000$0mh2uT2VZ9AHdhK5vyxbxH$I6JaVLravX8SQyw3eqSCx42UxyURdzDgg9ur1JtHdwE=','2025-10-13 23:19:21.458407',1,'admin','','','',1,1,'2025-10-12 14:05:10.947889');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `text` text NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `author_id` int NOT NULL,
  `painting_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `painting_id` (`painting_id`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`painting_id`) REFERENCES `painting` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,'Jako lep i izrazajan rad','2025-10-12 14:54:05',5,3),(2,'vau! kakva emocija','2025-10-12 14:54:36',5,4),(3,'Ovo me je inspirisalo da i ja naslikam nesto slicno.','2025-10-12 14:55:01',5,5),(4,'Odlicna slika, svidja mi se tehnika linija','2025-10-12 14:55:58',1,3),(5,'ledeno, brrrr','2025-10-12 15:12:31',1,1),(7,'Vau','2025-10-12 16:01:47',2,3),(8,'Imam i ja jednu slicnu, okacicu je','2025-10-12 16:02:13',2,4),(9,'lepo, ali nije naslikano','2025-10-12 16:20:53',3,6),(10,'vau kakav realizam.. kao da nije naslikano hmm','2025-10-12 16:21:26',3,1),(11,'ovo je prava prica. prelepo. stil, pokreti cetkicom, sve.. wow','2025-10-12 16:22:11',3,4),(12,'odlicna slika','2025-10-12 16:50:17',3,5),(13,'savetovao bih...','2025-10-12 16:51:05',3,7),(14,'jako mi se svidja','2025-10-13 00:18:36',1,3),(15,'svidja mi se!','2025-10-13 00:27:35',4,6);
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('4wvf0w9ozmretd2rxgnn42kx7ipyikz2','.eJxVjEEOgjAQRe_StWmm0JapS_eeoZnpDIIaSCisjHdXEha6_e-9_zKZtnXIW9Ulj2LOxpnT78ZUHjrtQO403WZb5mldRra7Yg9a7XUWfV4O9-9goDp8656AigsdQkDtsJRCKUCTYtQmtRiYlJgdgHrwbRQBD-KwAUWBntG8P-GRN70:1v7d24:3Pb7gLQitn8Hm6VqKrgABu57htu3FBRmhYF3UMGhYR4','2025-10-25 17:05:24.054500'),('5t7fglvuz1r1q8d65hd1x0pxiftn0vv2','.eJxVjEEOgjAQRe_StWmm0JapS_eeoZnpDIIaSCisjHdXEha6_e-9_zKZtnXIW9Ulj2LOxpnT78ZUHjrtQO403WZb5mldRra7Yg9a7XUWfV4O9-9goDp8656AigsdQkDtsJRCKUCTYtQmtRiYlJgdgHrwbRQBD-KwAUWBntG8P-GRN70:1v8R4i:QLnSrTGhDrZKAdKkkDgzMHG5CkAIsjbSPVe_qQrCiuM','2025-10-27 22:31:28.675289'),('d88p3ked8vmm62yq57qyw3d86666i75d','.eJxVjDsOwjAQBe_iGlk48WoxJT1nsLwf4wCypTipEHeHSCmgfTPzXiamdSlx7TrHSczZeHP43SjxQ-sG5J7qrVludZknsptid9rttYk-L7v7d1BSL9-aNLgMLJpxcOBGT46RYXQSIOdAAoqU9Qge0WtgYvYwsJxIRw8o5v0BBi041Q:1v7aJh:aAyG5LUZTvn_nNGhxSjJ2LnWq6L6GBnhKf8YgBJkn84','2025-10-25 14:11:25.320270'),('euf2kitvpovv1en3eqh4bx4ja78gdscb','.eJxVjEEOwiAQRe_C2hAoM9hx6d4zkBlAqRpISrsy3l2bdKHb_977LxV4XUpYe57DlNRJWaMOv6NwfOS6kXTnems6trrMk-hN0Tvt-tJSfp539--gcC_f-moZBZGctx4SeZeiYcfio4w0xDgSg0NLCT2AZXKIzoLJNMiROYN6fwD0BDdu:1v8Rvt:CIEgvtqAK6Fawax-4zrKo2XoVMAmUqE7nI4Xwy_YOcQ','2025-10-27 23:26:25.989285'),('zhnohe3x77z0friq1lwhowhafvn8jpv8','.eJxVjEEOgjAQRe_StWmm0JapS_eeoZnpDIIaSCisjHdXEha6_e-9_zKZtnXIW9Ulj2LOxpnT78ZUHjrtQO403WZb5mldRra7Yg9a7XUWfV4O9-9goDp8656AigsdQkDtsJRCKUCTYtQmtRiYlJgdgHrwbRQBD-KwAUWBntG8P-GRN70:1v8R6S:ETsRb98fLrbaoy4pm6Vg0BYkH7RrhP_9T1CIgRb-uSc','2025-10-27 22:33:16.707422');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exhibition`
--

DROP TABLE IF EXISTS `exhibition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exhibition` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `theme` varchar(100) NOT NULL,
  `description` text,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `status` enum('active','closed') NOT NULL DEFAULT 'active',
  `created_by` int NOT NULL,
  `winner_painting_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `winner_painting_id` (`winner_painting_id`),
  KEY `exhibition_ibfk_1` (`created_by`),
  CONSTRAINT `exhibition_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
  CONSTRAINT `exhibition_ibfk_2` FOREIGN KEY (`winner_painting_id`) REFERENCES `painting` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exhibition`
--

LOCK TABLES `exhibition` WRITE;
/*!40000 ALTER TABLE `exhibition` DISABLE KEYS */;
INSERT INTO `exhibition` VALUES (1,'Morski pejzaž','more','Slike mora i morskih predela, pejzaži prirode.','2025-10-11','2025-10-31','active',4,NULL),(2,'Oblici arhitekture','Arhitektura','Zanimljive zgrade i oblici','2025-10-12','2025-10-31','active',4,NULL),(3,'Lice emocije','osoba','Ljudi i prikaz njihove duse','2025-10-12','2025-10-31','active',4,NULL),(4,'Zimske čari','zima','Lepote zimskog perioda i osecaj koji izazivaju','2025-11-13','2025-11-30','closed',4,NULL);
/*!40000 ALTER TABLE `exhibition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `funding`
--

DROP TABLE IF EXISTS `funding`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `funding` (
  `id` int NOT NULL AUTO_INCREMENT,
  `amount` decimal(10,2) NOT NULL,
  `donor_id` int NOT NULL,
  `artist_id` int NOT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `donor_id` (`donor_id`),
  KEY `artist_id` (`artist_id`),
  CONSTRAINT `funding_ibfk_1` FOREIGN KEY (`donor_id`) REFERENCES `user` (`id`),
  CONSTRAINT `funding_ibfk_2` FOREIGN KEY (`artist_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funding`
--

LOCK TABLES `funding` WRITE;
/*!40000 ALTER TABLE `funding` DISABLE KEYS */;
INSERT INTO `funding` VALUES (1,100.00,1,2,'2025-10-12 15:19:48'),(2,5.00,2,4,'2025-10-12 15:33:51'),(3,2.00,4,1,'2025-10-14 00:58:26');
/*!40000 ALTER TABLE `funding` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `juryrequest`
--

DROP TABLE IF EXISTS `juryrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `juryrequest` (
  `id` int NOT NULL AUTO_INCREMENT,
  `applicant_id` int NOT NULL,
  `document_url` varchar(255) DEFAULT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `applicant_id` (`applicant_id`),
  CONSTRAINT `juryrequest_ibfk_1` FOREIGN KEY (`applicant_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `juryrequest`
--

LOCK TABLES `juryrequest` WRITE;
/*!40000 ALTER TABLE `juryrequest` DISABLE KEYS */;
INSERT INTO `juryrequest` VALUES (4,1,'/static/user_docs/minnie_oop_rand.txt','rejected','2025-10-12 16:13:42'),(5,4,'/static/user_docs/iloveart_CV.pdf','approved','2025-10-12 19:46:33'),(6,3,'/static/user_docs/marko2003_gitignore_global.txt','rejected','2025-10-14 01:16:29');
/*!40000 ALTER TABLE `juryrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `painting`
--

DROP TABLE IF EXISTS `painting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `painting` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `image_url` varchar(255) NOT NULL,
  `upload_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `artist_id` int NOT NULL,
  `avg_rating` float DEFAULT '0',
  `image_desc` text,
  PRIMARY KEY (`id`),
  KEY `artist_id` (`artist_id`),
  CONSTRAINT `painting_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `painting`
--

LOCK TABLES `painting` WRITE;
/*!40000 ALTER TABLE `painting` DISABLE KEYS */;
INSERT INTO `painting` VALUES (1,'Aheron reka','/static/img/ERXB0473_1760271160.JPG','2025-10-12 12:12:41',1,NULL,'Aheron reka sa temperaturom od 3 stepena'),(3,'Slutnja','/static/img/portret2_1760272976.jpg','2025-10-12 12:42:57',4,NULL,'Ulje na platnu prikazuje ženu uronjenu u misli, pogledom koji luta negde daleko — između nade i slutnje. Njen izraz lica odaje tihu napetost, kao da naslućuje nešto neizgovoreno, dok blage senke i topli tonovi ulja stvaraju osećaj intimne tišine i melanholije. Svetlost koja dodiruje njeno lice otkriva trenutak unutrašnje borbe između straha i slutnje, dok pozadina ostaje nejasna, kao maglovita scena iz sna.'),(4,'Starost','/static/img/portret1_1760273032.jpg','2025-10-12 12:43:53',4,NULL,'Ulje na platnu prikazuje starijeg muškarca čije lice nosi tragove vremena — svaka bora deluje kao zapis proživljenih dana. Pogled mu je dubok, miran, ali pun sećanja, dok ga meko svetlo obavija u tonovima sepije i senke. Umesto patetike, slika odiše dostojanstvom starosti i tihom mudrošću čoveka koji je mnogo video, a sada ćuti.'),(5,'Nebeski most','/static/img/watercolor-bridge_1760273147.jpg','2025-10-12 12:45:48',4,NULL,'Ulje na platnu prikazuje most obavijen plavičastim tonovima koji se stapaju s nebom, stvarajući utisak da se most ne uzdiže iznad reke, već lebdi između svetova. Svetlost i senke igraju se po njegovoj površini, brišući granicu između stvarnog i zamišljenog. Slika odiše spokojem i blagom melanholijom — kao da vodi ka mestu koje postoji samo u snu.'),(6,'Dete','/static/img/WhatsApp Image 2025-10-11 at 16.13.40_1760273302.jpeg','2025-10-12 12:48:22',2,NULL,''),(7,'Svetlost unutrasnje lepote','/static/img/womanpainting_1760273483.jpeg','2025-10-12 12:51:23',5,NULL,''),(8,'Romanticni zalazak','/static/img/sunset_1760291534.jpg','2025-10-12 17:52:14',5,NULL,'Naslikao sam ovo dok sam sedeo na plazi jednog letnjeg dana u Italiji..');
/*!40000 ALTER TABLE `painting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `participation`
--

DROP TABLE IF EXISTS `participation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `participation` (
  `painting_id` int NOT NULL,
  `exhibition_id` int NOT NULL,
  PRIMARY KEY (`painting_id`,`exhibition_id`),
  KEY `exhibition_id` (`exhibition_id`),
  CONSTRAINT `participation_ibfk_1` FOREIGN KEY (`painting_id`) REFERENCES `painting` (`id`),
  CONSTRAINT `participation_ibfk_2` FOREIGN KEY (`exhibition_id`) REFERENCES `exhibition` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `participation`
--

LOCK TABLES `participation` WRITE;
/*!40000 ALTER TABLE `participation` DISABLE KEYS */;
INSERT INTO `participation` VALUES (1,1),(8,1),(5,2),(3,3),(4,3),(6,3),(7,3);
/*!40000 ALTER TABLE `participation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rating`
--

DROP TABLE IF EXISTS `rating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rating` (
  `id` int NOT NULL AUTO_INCREMENT,
  `score` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `author_id` int NOT NULL,
  `painting_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `author_id` (`author_id`,`painting_id`),
  KEY `painting_id` (`painting_id`),
  CONSTRAINT `rating_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`),
  CONSTRAINT `rating_ibfk_2` FOREIGN KEY (`painting_id`) REFERENCES `painting` (`id`),
  CONSTRAINT `rating_chk_1` CHECK ((`score` between 1 and 5))
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rating`
--

LOCK TABLES `rating` WRITE;
/*!40000 ALTER TABLE `rating` DISABLE KEYS */;
INSERT INTO `rating` VALUES (2,5,'2025-10-12 14:53:58',5,3),(3,5,'2025-10-12 14:54:27',5,4),(4,5,'2025-10-12 14:55:30',1,3),(5,4,'2025-10-12 14:56:14',1,7),(6,5,'2025-10-12 15:12:03',1,1),(7,5,'2025-10-12 15:15:08',1,6),(8,5,'2025-10-12 16:01:43',2,3),(9,5,'2025-10-12 16:01:59',2,4),(10,4,'2025-10-12 16:20:41',3,6),(11,3,'2025-10-12 16:50:39',3,7),(12,2,'2025-10-12 19:52:47',5,1),(15,5,'2025-10-13 00:27:08',4,6);
/*!40000 ALTER TABLE `rating` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `role` enum('guest','registered','jury','admin') NOT NULL DEFAULT 'guest',
  `bio` text,
  `date_joined` datetime DEFAULT CURRENT_TIMESTAMP,
  `pfp_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'minnie','Pass123!','mina.sljivic@gmail.com','Mina','Sljivic','registered','Ja sam mina, ne umem da slikam i crtam, pa cu kaciti svoje slike sa mora koje imam na laptopu :)','2025-10-11 15:54:07','/static/img/minnie.JPG'),(2,'stole','stole123','stojan.sljivic@gmail.com','Stojan','Sljivic','registered','Ja sam Stojan, Minin tata i ja cu da kacim svoje fotografije ovde, ja fotografisem amaterski.','2025-10-11 15:58:16','/static/img/stole.jpeg'),(3,'marko2003','mare12345','mare@gmail','Marko','Markovic','registered','','2025-10-11 16:02:05',NULL),(4,'iloveart','iloveart','kosta@email','Kosta','Kovacevic','jury','ja sam pro','2025-10-11 16:03:32','/static/img/iloveart.jpg'),(5,'reks','reks12345','reks@email','Relja','Popovic','registered','Ja sam reks','2025-10-11 16:05:10','/static/img/reks.webp'),(6,'admin','admin123','admin@email','Admin','Adminic','admin',NULL,NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-14  1:33:35
