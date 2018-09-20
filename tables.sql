-- phpMyAdmin SQL Dump
-- version 4.7.9
-- https://www.phpmyadmin.net/
--
-- 主機: localhost:3306
-- 產生時間： 2018 年 09 月 20 日 03:18
-- 伺服器版本: 10.2.17-MariaDB
-- PHP 版本： 7.1.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+08:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `Hua777`
--

-- --------------------------------------------------------

--
-- 資料表結構 `classes`
--

CREATE TABLE `classes` (
  `Id` bigint(20) NOT NULL,
  `Change` text CHARACTER SET utf8 NOT NULL,
  `Description` text CHARACTER SET utf8 NOT NULL,
  `MultipleCompulsory` text CHARACTER SET utf8 NOT NULL,
  `Department` text CHARACTER SET utf8 NOT NULL,
  `SDepartment` text CHARACTER SET utf8 NOT NULL,
  `Number` text CHARACTER SET utf8 NOT NULL,
  `Grade` text CHARACTER SET utf8 NOT NULL,
  `Class` text CHARACTER SET utf8 NOT NULL,
  `Name` text CHARACTER SET utf8 NOT NULL,
  `SName` text CHARACTER SET utf8 NOT NULL,
  `Url` text CHARACTER SET utf8 NOT NULL,
  `Credit` text CHARACTER SET utf8 NOT NULL,
  `YearSemester` text CHARACTER SET utf8 NOT NULL,
  `CompulsoryElective` text CHARACTER SET utf8 NOT NULL,
  `Restrict` text CHARACTER SET utf8 NOT NULL,
  `Select` text CHARACTER SET utf8 NOT NULL,
  `Selected` text CHARACTER SET utf8 NOT NULL,
  `Remaining` text CHARACTER SET utf8 NOT NULL,
  `Teacher` text CHARACTER SET utf8 NOT NULL,
  `STeacher` text CHARACTER SET utf8 NOT NULL,
  `Room` text CHARACTER SET utf8 NOT NULL,
  `Monday` text CHARACTER SET utf8 NOT NULL,
  `Tuesday` text CHARACTER SET utf8 NOT NULL,
  `Wednesday` text CHARACTER SET utf8 NOT NULL,
  `Thursday` text CHARACTER SET utf8 NOT NULL,
  `Friday` text CHARACTER SET utf8 NOT NULL,
  `Saturday` text CHARACTER SET utf8 NOT NULL,
  `Sunday` text CHARACTER SET utf8 NOT NULL,
  `Context` text CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 資料表結構 `feedbacks`
--

CREATE TABLE `feedbacks` (
  `Id` bigint(20) NOT NULL,
  `Name` text NOT NULL,
  `Email` text NOT NULL,
  `Subject` text NOT NULL,
  `Message` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 已匯出資料表的索引
--

--
-- 資料表索引 `classes`
--
ALTER TABLE `classes`
  ADD PRIMARY KEY (`Id`);

--
-- 資料表索引 `feedbacks`
--
ALTER TABLE `feedbacks`
  ADD PRIMARY KEY (`Id`);

--
-- 在匯出的資料表使用 AUTO_INCREMENT
--

--
-- 使用資料表 AUTO_INCREMENT `classes`
--
ALTER TABLE `classes`
  MODIFY `Id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表 AUTO_INCREMENT `feedbacks`
--
ALTER TABLE `feedbacks`
  MODIFY `Id` bigint(20) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
