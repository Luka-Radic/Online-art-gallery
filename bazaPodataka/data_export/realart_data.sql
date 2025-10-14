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
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$DfTurEcpgib1U4gTheaKSh$kNHoTuWe/xIy5R+wu/1LnMG4zqDPsr+yQBUIpwr268o=','2025-10-12 17:49:25.452553',0,'minnie','','','',0,1,'2025-10-11 13:54:07.695107'),(2,'pbkdf2_sha256$1000000$NYdswgOhqDPrComMq9xKRV$AANZ94Yb2d8UPYuAN/FbgUAxanSGVtFommYeCrurCAQ=','2025-10-12 13:22:45.480727',0,'stole','','','',0,1,'2025-10-11 13:58:16.968988'),(3,'pbkdf2_sha256$1000000$QAe5xrkGPp9gOuSJ5h0hm5$fJL2XUv8BbK42VEyg4F/0WAx2x1fpw2b2tBf0yPmU4U=','2025-10-12 14:20:29.715598',0,'marko2003','','','',0,1,'2025-10-11 14:02:05.864076'),(4,'pbkdf2_sha256$1000000$jhye9W6paxTxYP9kGL0KOm$qPiiUMaeUTXTGmEAlLrQiWBszGql+wTAIXvKYe3Gj4Q=','2025-10-12 17:45:55.303095',0,'iloveart','','','',0,1,'2025-10-11 14:03:32.895488'),(5,'pbkdf2_sha256$1000000$VXVu7wzkd05zAPqNn4H1z7$EoS69nWNPUuEiqLdL4S0p2bRqq8RvMmmx+zu/HOs5vE=','2025-10-12 17:50:36.994388',0,'reks','','','',0,1,'2025-10-11 14:05:10.935807'),(6,'pbkdf2_sha256$1000000$0mh2uT2VZ9AHdhK5vyxbxH$I6JaVLravX8SQyw3eqSCx42UxyURdzDgg9ur1JtHdwE=','2025-10-12 18:04:02.512316',1,'admin','','','',1,1,'2025-10-12 14:05:10.947889');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,'Jako lep i izrazajan rad','2025-10-12 14:54:05',5,3),(2,'vau! kakva emocija','2025-10-12 14:54:36',5,4),(3,'Ovo me je inspirisalo da i ja naslikam nesto slicno.','2025-10-12 14:55:01',5,5),(4,'Odlicna slika, svidja mi se tehnika linija','2025-10-12 14:55:58',1,3),(5,'ledeno, brrrr','2025-10-12 15:12:31',1,1),(7,'Vau','2025-10-12 16:01:47',2,3),(8,'Imam i ja jednu slicnu, okacicu je','2025-10-12 16:02:13',2,4),(9,'lepo, ali nije naslikano','2025-10-12 16:20:53',3,6),(10,'vau kakav realizam.. kao da nije naslikano hmm','2025-10-12 16:21:26',3,1),(11,'ovo je prava prica. prelepo. stil, pokreti cetkicom, sve.. wow','2025-10-12 16:22:11',3,4),(12,'odlicna slika','2025-10-12 16:50:17',3,5),(13,'savetovao bih...','2025-10-12 16:51:05',3,7);
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('4wvf0w9ozmretd2rxgnn42kx7ipyikz2','.eJxVjEEOgjAQRe_StWmm0JapS_eeoZnpDIIaSCisjHdXEha6_e-9_zKZtnXIW9Ulj2LOxpnT78ZUHjrtQO403WZb5mldRra7Yg9a7XUWfV4O9-9goDp8656AigsdQkDtsJRCKUCTYtQmtRiYlJgdgHrwbRQBD-KwAUWBntG8P-GRN70:1v7d24:3Pb7gLQitn8Hm6VqKrgABu57htu3FBRmhYF3UMGhYR4','2025-10-25 17:05:24.054500'),('d88p3ked8vmm62yq57qyw3d86666i75d','.eJxVjDsOwjAQBe_iGlk48WoxJT1nsLwf4wCypTipEHeHSCmgfTPzXiamdSlx7TrHSczZeHP43SjxQ-sG5J7qrVludZknsptid9rttYk-L7v7d1BSL9-aNLgMLJpxcOBGT46RYXQSIOdAAoqU9Qge0WtgYvYwsJxIRw8o5v0BBi041Q:1v7aJh:aAyG5LUZTvn_nNGhxSjJ2LnWq6L6GBnhKf8YgBJkn84','2025-10-25 14:11:25.320270');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `exhibition`
--

LOCK TABLES `exhibition` WRITE;
/*!40000 ALTER TABLE `exhibition` DISABLE KEYS */;
INSERT INTO `exhibition` VALUES (1,'Morski pejzaž','more','Slike mora i morskih predela, pejzaži prirode.','2025-10-11','2025-10-31','active',4,NULL),(2,'Oblici arhitekture','Arhitektura','Zanimljive zgrade i oblici','2025-10-12','2025-10-31','active',4,NULL),(3,'Lice emocije','osoba','Ljudi i prikaz njihove duse','2025-10-12','2025-10-31','active',4,NULL),(4,'Zimske čari','zima','Lepote zimskog perioda i osecaj koji izazivaju','2025-11-13','2025-11-30','closed',4,NULL);
/*!40000 ALTER TABLE `exhibition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `funding`
--

LOCK TABLES `funding` WRITE;
/*!40000 ALTER TABLE `funding` DISABLE KEYS */;
INSERT INTO `funding` VALUES (1,100.00,1,2,'2025-10-12 15:19:48'),(2,5.00,2,4,'2025-10-12 15:33:51');
/*!40000 ALTER TABLE `funding` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `juryrequest`
--

LOCK TABLES `juryrequest` WRITE;
/*!40000 ALTER TABLE `juryrequest` DISABLE KEYS */;
INSERT INTO `juryrequest` VALUES (4,1,'/static/user_docs/minnie_oop_rand.txt','rejected','2025-10-12 16:13:42'),(5,4,'/static/user_docs/iloveart_CV.pdf','approved','2025-10-12 19:46:33');
/*!40000 ALTER TABLE `juryrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `painting`
--

LOCK TABLES `painting` WRITE;
/*!40000 ALTER TABLE `painting` DISABLE KEYS */;
INSERT INTO `painting` VALUES (1,'Aheron reka','/static/img/ERXB0473_1760271160.JPG','2025-10-12 12:12:41',1,NULL,'Aheron reka sa temperaturom od 3 stepena'),(3,'Slutnja','/static/img/portret2_1760272976.jpg','2025-10-12 12:42:57',4,NULL,'Ulje na platnu prikazuje ženu uronjenu u misli, pogledom koji luta negde daleko — između nade i slutnje. Njen izraz lica odaje tihu napetost, kao da naslućuje nešto neizgovoreno, dok blage senke i topli tonovi ulja stvaraju osećaj intimne tišine i melanholije. Svetlost koja dodiruje njeno lice otkriva trenutak unutrašnje borbe između straha i slutnje, dok pozadina ostaje nejasna, kao maglovita scena iz sna.'),(4,'Starost','/static/img/portret1_1760273032.jpg','2025-10-12 12:43:53',4,NULL,'Ulje na platnu prikazuje starijeg muškarca čije lice nosi tragove vremena — svaka bora deluje kao zapis proživljenih dana. Pogled mu je dubok, miran, ali pun sećanja, dok ga meko svetlo obavija u tonovima sepije i senke. Umesto patetike, slika odiše dostojanstvom starosti i tihom mudrošću čoveka koji je mnogo video, a sada ćuti.'),(5,'Nebeski most','/static/img/watercolor-bridge_1760273147.jpg','2025-10-12 12:45:48',4,NULL,'Ulje na platnu prikazuje most obavijen plavičastim tonovima koji se stapaju s nebom, stvarajući utisak da se most ne uzdiže iznad reke, već lebdi između svetova. Svetlost i senke igraju se po njegovoj površini, brišući granicu između stvarnog i zamišljenog. Slika odiše spokojem i blagom melanholijom — kao da vodi ka mestu koje postoji samo u snu.'),(6,'Dete','/static/img/WhatsApp Image 2025-10-11 at 16.13.40_1760273302.jpeg','2025-10-12 12:48:22',2,NULL,''),(7,'Svetlost unutrasnje lepote','/static/img/womanpainting_1760273483.jpeg','2025-10-12 12:51:23',5,NULL,''),(8,'Romanticni zalazak','/static/img/sunset_1760291534.jpg','2025-10-12 17:52:14',5,NULL,'Naslikao sam ovo dok sam sedeo na plazi jednog letnjeg dana u Italiji..');
/*!40000 ALTER TABLE `painting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `participation`
--

LOCK TABLES `participation` WRITE;
/*!40000 ALTER TABLE `participation` DISABLE KEYS */;
INSERT INTO `participation` VALUES (1,1),(8,1),(5,2),(3,3),(4,3),(6,3),(7,3);
/*!40000 ALTER TABLE `participation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `rating`
--

LOCK TABLES `rating` WRITE;
/*!40000 ALTER TABLE `rating` DISABLE KEYS */;
INSERT INTO `rating` VALUES (2,5,'2025-10-12 14:53:58',5,3),(3,5,'2025-10-12 14:54:27',5,4),(4,5,'2025-10-12 14:55:30',1,3),(5,4,'2025-10-12 14:56:14',1,7),(6,5,'2025-10-12 15:12:03',1,1),(7,5,'2025-10-12 15:15:08',1,6),(8,5,'2025-10-12 16:01:43',2,3),(9,5,'2025-10-12 16:01:59',2,4),(10,4,'2025-10-12 16:20:41',3,6),(11,3,'2025-10-12 16:50:39',3,7),(12,2,'2025-10-12 19:52:47',5,1);
/*!40000 ALTER TABLE `rating` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'minnie','Pass123!','mina.sljivic@gmail.com','Mina','Sljivic','registered','Ja sam mina, ne umem da slikam i crtam, pa cu kaciti svoje slike sa mora koje imam na laptopu :)','2025-10-11 15:54:07','/static/img/minnie.JPG'),(2,'stole','stole123','stojan.sljivic@gmail.com','Stojan','Sljivic','registered','Ja sam Stojan, Minin tata i ja cu da kacim svoje fotografije ovde, ja fotografisem amaterski.','2025-10-11 15:58:16','/static/img/stole.jpeg'),(3,'marko2003','mare12345','mare@email','Marko','Markovic','registered','','2025-10-11 16:02:05',NULL),(4,'iloveart','iloveart','kosta@email','Kosta','Kovacevic','jury','ja sam pro','2025-10-11 16:03:32','/static/img/iloveart.jpg'),(5,'reks','reks12345','reks@email','Relja','Popovic','registered','Ja sam reks','2025-10-11 16:05:10','/static/img/reks.webp'),(6,'admin','admin123','admin@email','Admin','Adminic','admin',NULL,NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'realart'
--

--
-- Dumping routines for database 'realart'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-12 20:09:01
