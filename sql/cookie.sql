CREATE TABLE `cookie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cookie_str` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `account` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  `cuid` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`,`uid`,`account`,`cuid`) USING BTREE,
  UNIQUE KEY `id` (`id`) USING BTREE,
  UNIQUE KEY `uid` (`uid`),
  UNIQUE KEY `account` (`account`) USING BTREE,
  UNIQUE KEY `cuid` (`cuid`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;