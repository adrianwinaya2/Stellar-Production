SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `stellar_account` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `stellar_account`;

-- ! ACCOUNT TABLE
CREATE TABLE `Account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(200) NOT NULL,
  `role` ENUM('Staff', 'Client') NOT NULL,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `Account` (`username`, `password`, `role`) VALUES
('adrian123', 'adrian123', 'Staff'),
('winaya456', 'winaya456', 'Staff'),
('jefry123', 'jefry123', 'Staff'),
('gunawan456', 'gunawan456', 'Staff'),

('budi123', 'budi123', 'Client'),
('wawan456', 'wawan456', 'Client'),
('agus789', 'agus789', 'Client');

COMMIT;

