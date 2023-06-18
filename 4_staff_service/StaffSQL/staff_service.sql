SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `stellar_staff` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `stellar_staff`;

-- ! STAFF TABLE
CREATE TABLE `Staff` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  'username' varchar(20) NOT NULL
  `name` varchar(200) NOT NULL,
  `email` varchar(50) NOT NULL,
  `position` ENUM('Leader', 'Coordinator', 'Member') NOT NULL,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `Staff` (`username`, `name`, `email`, `position`) VALUES
('adrian123', 'Adrian', 'adrian@gmail.com', 'Leader'),
('winaya456', 'Winaya', 'winaya@gmail.com', 'Member'),
('jefry123', 'Jefry', 'jefry@gmail.com', 'Coordinator'),
('gunawan456', 'Gunawan', 'gunawan@gmail.com', 'Member');

COMMIT;
