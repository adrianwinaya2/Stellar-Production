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
  `phone` varchar(15) NOT NULL,
  `position` ENUM('Leader', 'Coordinator', 'Member') NOT NULL,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `Staff` (`username`, `name`, `phone`, `position`) VALUES
('adrian123', 'Adrian', '084', 'Leader'),
('winaya456', 'Winaya', '085', 'Member'),
('jefry123', 'Jefry', '086', 'Coordinator'),
('gunawan456', 'Gunawan', '087', 'Member');

COMMIT;

