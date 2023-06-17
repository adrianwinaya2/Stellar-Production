SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `stellar_client` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `stellar_client`;

-- ! CLIENT TABLE
CREATE TABLE `Client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  'username' varchar(20) NOT NULL
  `name` varchar(200) NOT NULL,
  `phone` varchar(15) NOT NULL,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `Client` (`username`, `name`, `email`) VALUES
('budi123', 'Budi', 'budi@gmail.com'),
('wawan456', 'Wawan', 'wawan@gmail.com'),
('agus789', 'Agus', 'agus@gmail.com');

COMMIT;

