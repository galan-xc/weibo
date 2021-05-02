CREATE TABLE `cmt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wid` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `comment_id` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `comment_create` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comment_text` varchar(1200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_profile` varchar(600) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_verified` smallint(6) DEFAULT '0',
  `user_verified_reason` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_description` varchar(450) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gender` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `statuses_count` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `source` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;