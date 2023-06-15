SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `stellar_event` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `stellar_event`;

-- ! ORDER TABLE
CREATE TABLE `Order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `schedule` DATETIME NOT NULL,

  PRIMARY KEY (`id`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `Order` (`name`, `schedule`) VALUES
('Ana & Anu', '2023-06-10 10:00:00'),
('Jennifer', '2023-06-11 11:00:00'),
('David', '2023-06-12 12:00:00');

-- ! STAFF TABLE
CREATE TABLE `Staff` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `position` varchar(11) NOT NULL ENUM('Leader', 'Coordinator', 'Member') DEFAULT 'member',

  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `Staff` (`name`, `position`) VALUES
('Adrian', 'Leader'),
('Winaya', 'Member'),
('Jefry', 'Coordinator'),
('Gunawan', 'Member');

-- ! EVENT TABLE
CREATE TABLE `Event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL,
  `pic_id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `time_start` TIME NOT NULL,
  `time_end` TIME NOT NULL,

  PRIMARY KEY (`id`),
  FOREIGN KEY (`order_id`) REFERENCES `Order` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`pic_id`) REFERENCES `Staff` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `Event` (`order_id`, `pic_id`, `name`, `time_start`, `time_end`) VALUES
(0, 0, 'Opening', '10:00:00', '10:05:00'),
(0, 1, 'Photo Session', '10:05:00', '10:10:00'),
(0, 2, 'Games', '10:10:00', '10:50:00'),
(0, 3, 'Opening', '10:50:00', '11:00:00'),

(1, 0, 'Opening', '11:00:00', '11:05:00'),
(1, 1, 'Photo Session', '11:05:00', '11:10:00'),
(1, 2, 'Games', '11:10:00', '11:50:00'),
(1, 3, 'Opening', '11:50:00', '12:00:00'),

(2, 0, 'Opening', '11:00:00', '11:05:00'),
(2, 1, 'Photo Session', '11:05:00', '11:10:00'),
(2, 2, 'Games', '11:10:00', '11:50:00'),
(2, 3, 'Opening', '11:50:00', '12:00:00');


COMMIT;

