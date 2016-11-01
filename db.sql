-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        10.1.14-MariaDB - mariadb.org binary distribution
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  9.1.0.4867
-- --------------------------------------------------------

-- 导出 music_db 的数据库结构
DROP DATABASE IF EXISTS `music_db`;
CREATE DATABASE IF NOT EXISTS `music_db` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
USE `music_db`;


-- 导出  表 music_db.clips 结构
DROP TABLE IF EXISTS `clips`;
CREATE TABLE IF NOT EXISTS `clips` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` tinyint(4) NOT NULL,
  `bpm` float NOT NULL,
  `path` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 导出  表 music_db.info 结构
DROP TABLE IF EXISTS `info`;
CREATE TABLE IF NOT EXISTS `info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `time` float NOT NULL,
  `style` text NOT NULL,
  `bpm` float NOT NULL,
  `key` tinyint(3) unsigned NOT NULL,
  `music_path` varchar(255) NOT NULL,
  `beat_path` varchar(255) NOT NULL,
  `info_path` varchar(255) NOT NULL,
  `chord_path` varchar(255) NOT NULL,
  `type` int(11) NOT NULL,
  `avaliable` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 导出  表 music_db.match_matrices 结构
DROP TABLE IF EXISTS `match_matrices`;
CREATE TABLE IF NOT EXISTS `match_matrices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `music_id` int(11) NOT NULL,
  `clip_matrix_path` varchar(255) NOT NULL,
  `score_matrix_path` varchar(255)  NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
