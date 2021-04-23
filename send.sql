CREATE TABLE `send` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `msg` varchar(800) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ret` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;