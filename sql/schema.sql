use test;

CREATE TABLE `HelpDesk_Ticket` (
  `ticket_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` varchar(50) NOT NULL,
  `subject` text,
  `content` text,
  `asignee_id` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_date` datetime NOT NULL,
  PRIMARY KEY (`ticket_id`)
);

CREATE TABLE `HelpDesk_Ticket_History` (
  `ticket_id` int(11) NOT NULL,
  `customer_id` varchar(50) NOT NULL,
  `subject` text,
  `content` text,
  `asignee_id` varchar(50) DEFAULT NULL,
  `status` varchar(50) NOT NULL,
  `content_update_by` varchar(50) NOT NULL,
  `created_date` datetime NOT NULL
);

CREATE TABLE `HelpDesk_User` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `user_type` varchar(25) DEFAULT NULL,
  `firstname` varchar(80) NOT NULL,
  `lastname` varchar(80) NOT NULL,
  `email_id` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_id` (`email_id`)
);

CREATE TABLE `HelpDesk_Staff` (
  `staff_id` int(11) NOT NULL,
  `number_of_tickets` int(11) DEFAULT '0',
  `updated_date` datetime NOT NULL
);

CREATE TABLE `HelpDesk_Staff_TicketHistory` (
  `staff_id` int(11) NOT NULL,
  `ticket_id` int(11) DEFAULT NULL,
  `assigned_date` datetime NOT NULL,
  `completed_date` datetime DEFAULT NULL
);
