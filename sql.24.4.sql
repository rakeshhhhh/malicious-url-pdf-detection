/*
SQLyog Community v13.1.5  (64 bit)
MySQL - 5.6.12-log : Database - phishing
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`phishing` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `phishing`;

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `Complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `User_id` int(11) DEFAULT NULL,
  `Complaint` varchar(50) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `Status` varchar(50) DEFAULT NULL,
  `Reply` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Complaint_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`Complaint_id`,`User_id`,`Complaint`,`Date`,`Time`,`Status`,`Reply`) values 
(1,1,'fgvhbgu','2023-04-04','00:00:02','Replied','too slow'),
(2,4,'vgjhkkkmmmm','2023-04-12','13:13:33','Replied','ok'),
(3,4,'gyghkjh','2023-04-17','13:05:14','Replied','fgsgger'),
(4,4,'hvjfuygi','2023-04-17','20:05:45','Replied','fregerge'),
(5,4,'','2023-04-24','02:12:48','Replied','is it ok');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `Feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `User_id` int(11) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `Feedback` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Feedback_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`Feedback_id`,`User_id`,`Date`,`Time`,`Feedback`) values 
(1,1,'2023-04-10','00:00:01','Good'),
(2,4,'2023-04-12','13:00:38','cfcgvhb'),
(3,4,'2023-04-17','13:05:22','jgjgiukk'),
(4,4,'2023-04-17','20:05:57','gyuiugo');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `Login_id` int(11) NOT NULL AUTO_INCREMENT,
  `User_name` varchar(30) DEFAULT NULL,
  `Password` varchar(30) DEFAULT NULL,
  `User_type` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`Login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`Login_id`,`User_name`,`Password`,`User_type`) values 
(1,'admin@gmail.com','123','admin'),
(2,'u@g','0','user'),
(4,'anu@g','anu','user');

/*Table structure for table `tips` */

DROP TABLE IF EXISTS `tips`;

CREATE TABLE `tips` (
  `Tip_id` int(11) NOT NULL AUTO_INCREMENT,
  `Tips` varchar(50) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  PRIMARY KEY (`Tip_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `tips` */

insert  into `tips`(`Tip_id`,`Tips`,`Date`) values 
(4,'Internet connection','2023-04-10'),
(5,'gud to use','2023-04-17'),
(8,'dsdsdad','2023-04-17');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `User_id` int(11) NOT NULL AUTO_INCREMENT,
  `Login_id` int(11) DEFAULT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `Pin` int(50) DEFAULT NULL,
  `District` varchar(50) DEFAULT NULL,
  `Phone_no` bigint(11) DEFAULT NULL,
  `Gender` varchar(11) DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`User_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`User_id`,`Login_id`,`Name`,`place`,`post`,`Pin`,`District`,`Phone_no`,`Gender`,`Email`) values 
(1,1,'Aneesh','Thennala','post',676508,'Malappram',8086351800,'Male','aneeshkk12@gmail.com'),
(3,4,'Anusree','nadakkav','naddakkav',123456,'calicut',9876543210,'Female','anu@g');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
