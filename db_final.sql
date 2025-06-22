/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 5.7.9 : Database - blockchain_for_decentralized_storage
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`blockchain_for_decentralized_storage` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `blockchain_for_decentralized_storage`;

/*Table structure for table `complaints` */

DROP TABLE IF EXISTS `complaints`;

CREATE TABLE `complaints` (
  `complaints_id` int(10) NOT NULL AUTO_INCREMENT,
  `user_id` int(10) DEFAULT NULL,
  `title` varchar(500) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `reply` varchar(500) DEFAULT NULL,
  `date` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`complaints_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `complaints` */

insert  into `complaints`(`complaints_id`,`user_id`,`title`,`description`,`reply`,`date`) values 
(1,1,'new','fghbnjmk','Earum enim vel ad du','19-12-2024'),
(2,1,'Ex dolores ipsa cul','Fugiat consequat Ci','Id non autem culpa r','2024-12-20'),
(3,1,'Voluptas magnam sed ','Iusto dolor repudian','pending','2024-12-30'),
(4,1,'Sunt ut placeat max','Necessitatibus offic','pending','2024-12-30'),
(5,1,'Death ','i died',',mn','2025-01-02');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(500) DEFAULT NULL,
  `password` varchar(500) DEFAULT NULL,
  `usertype` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values 
(1,'admin','admin','admin'),
(2,'user','123','user'),
(3,'user1','123','user'),
(4,'user2','123','user'),
(5,'user3','123','user'),
(6,'Louis Wilkerson','Pa$$w0rd!','user'),
(7,'dd','300','user'),
(8,'Nora Lancaster','12345678@','user');

/*Table structure for table `notification` */

DROP TABLE IF EXISTS `notification`;

CREATE TABLE `notification` (
  `notification_id` int(10) NOT NULL AUTO_INCREMENT,
  `title` varchar(500) DEFAULT NULL,
  `decription` varchar(500) DEFAULT NULL,
  `date` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`notification_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `notification` */

insert  into `notification`(`notification_id`,`title`,`decription`,`date`) values 
(1,'Et commodo at omnis ','Odit molestias perfe','2024-12-19'),
(2,'Death ','dfgh','2024-12-20'),
(3,'Quia totam quibusdam','Hic aut sit natus ve','2024-12-30'),
(4,'Ipsum perspiciatis ','In a fugiat explica','2024-12-30'),
(5,'Doloremque voluptas ','Ad aliqua Repudiand','2025-01-02');

/*Table structure for table `system_details` */

DROP TABLE IF EXISTS `system_details`;

CREATE TABLE `system_details` (
  `system_details_id` int(10) NOT NULL AUTO_INCREMENT,
  `user_id` int(10) DEFAULT NULL,
  `system_name` varchar(500) DEFAULT NULL,
  `system_password` varchar(500) DEFAULT NULL,
  `system_user_name` varchar(500) DEFAULT NULL,
  `file_name` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`system_details_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `system_details` */

insert  into `system_details`(`system_details_id`,`user_id`,`system_name`,`system_password`,`system_user_name`,`file_name`) values 
(1,2,'DESKTOP-SJA5CTD','Riss@2024','desktop-sja5ctd\\riss thrissur','Files_Share'),
(2,3,'DESKTOP-MGN0N1Q','@RissTechnologies','desktop-mgn0n1q\\risst','New_File_Share'),
(5,1,'Xena Duffy','Pa$$w0rd!','Kadeem Pierce','Quon Stevenson');

/*Table structure for table `upload_file` */

DROP TABLE IF EXISTS `upload_file`;

CREATE TABLE `upload_file` (
  `upload_file_id` int(10) NOT NULL AUTO_INCREMENT,
  `user_id` int(10) DEFAULT NULL,
  `system_details_first_id` int(10) DEFAULT NULL,
  `system_details_second_id` int(10) DEFAULT NULL,
  `title` varchar(500) DEFAULT NULL,
  `system_one` varchar(500) DEFAULT NULL,
  `system_two` varchar(500) DEFAULT NULL,
  `part_one` varchar(500) DEFAULT NULL,
  `part_two` varchar(500) DEFAULT NULL,
  `date` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`upload_file_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `upload_file` */

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(10) NOT NULL AUTO_INCREMENT,
  `login_id` int(10) DEFAULT NULL,
  `fname` varchar(500) DEFAULT NULL,
  `lname` varchar(500) DEFAULT NULL,
  `phone` varchar(500) DEFAULT NULL,
  `email` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`login_id`,`fname`,`lname`,`phone`,`email`) values 
(1,2,'Lysandra','Coffey','+1 (525) 522-9415','gasyjuhik@mailinator.com'),
(2,3,'Vernon Mullen','Stewart Ferrell','Officia enim eligend','dycatar@mailinator.com'),
(3,4,'Ann Benjamin','Caryn Hahn','Voluptas omnis anim ','wexa@mailinator.com'),
(4,5,'Sarah Bullock','Urielle Austin','Eos ut dolorem qui n','cawupynal@mailinator.com'),
(5,6,'Abigail Becker','Katell Hart','Sapiente optio aute','jedibugur@mailinator.com'),
(6,7,'456','879','dghjkj','scott100@gmail.com'),
(7,8,'Jason Russell','Daryl Young','1987717159','suja@mailinator.com');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
