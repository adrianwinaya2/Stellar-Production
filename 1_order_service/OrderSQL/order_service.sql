SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `stellar_order` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `stellar_order`;

-- ! CLIENT TABLE
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

-- ! ORDER TABLE
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
(0, 0, 'Ana & Anu', 'Wedding', '2023-06-10 10:00:00', 'Done'),
(1, 1, 'Jennifer', 'Sweet 17', '2023-06-11 11:00:00', 'Cancelled'),
(2, 2, 'David', 'Birthday', '2023-06-12 12:00:00', 'Scheduled');
-- (1, 2, 'Matthew', 'Birthday', '2023-06-13 13:00:00', 'Done'),
-- (1, 3, 'Patricia', 'Birthday', '2023-06-14 14:00:00', 'Cancelled'),
-- (2, 1, 'Lala & Lolo', 'Wedding', '2023-06-15 15:00:00', 'Scheduled'),
-- (2, 2, 'Catherine', 'Sweet 17', '2023-06-16 16:00:00', 'Scheduled');


-- ALTER TABLE `kantin_menu`
--   ADD PRIMARY KEY (`id`),
--   ADD KEY `idresto` (`idresto`);

-- ALTER TABLE `kantin_resto`
--   ADD PRIMARY KEY (`id`);

-- ALTER TABLE `kantin_menu`
--   MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

-- ALTER TABLE `kantin_resto`
--   MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

-- ALTER TABLE `kantin_menu`
--   ADD CONSTRAINT `kantin_menu_ibfk_1` FOREIGN KEY (`idresto`) REFERENCES `kantin_resto` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

COMMIT;

