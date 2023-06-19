SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `stellar_order` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `stellar_order`;

-- CLIENT TABLE
CREATE TABLE `Client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `phone` varchar(15) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `Client` (`name`, `phone`) VALUES
('Budi', '083'),
('Wawan', '082'),
('Agus', '081');

-- STAFF TABLE
CREATE TABLE `Staff` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `position` ENUM('Leader', 'Coordinator', 'Member') NOT NULL DEFAULT 'Member',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `Staff` (`name`, `position`) VALUES
('Adrian', 'Leader'),
('Winaya', 'Member'),
('Jefry', 'Coordinator'),
('Gunawan', 'Member');

-- ORDER TABLE
CREATE TABLE `Order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `pic_id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `category` ENUM('Sweet 17', 'Wedding', 'Birthday') NOT NULL,
  `schedule` DATETIME NOT NULL,
  `status` ENUM('Done', 'Cancelled', 'Scheduled') DEFAULT 'Scheduled',
  PRIMARY KEY (`id`),
  FOREIGN KEY (`client_id`) REFERENCES `Client` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`pic_id`) REFERENCES `Staff` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `Order` (`client_id`, `pic_id`, `name`, `category`, `schedule`, `status`) VALUES
(1, 1, 'Ana & Anu', 'Wedding', '2023-06-10 10:00:00', 'Done'),
(2, 2, 'Jennifer', 'Sweet 17', '2023-06-11 11:00:00', 'Cancelled'),
(3, 3, 'David', 'Birthday', '2023-06-12 12:00:00', 'Scheduled');

COMMIT;
