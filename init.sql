-- 数据库初始化脚本
CREATE DATABASE If Not Exists `funds`;
USE funds;

-- 创建数据库表
CREATE TABLE If Not Exists `funds_list` (
    `FundCode` VARCHAR(30) PRIMARY KEY,
    `ShortName` VARCHAR(30),
    `FullName` VARCHAR(100),
    `Type` VARCHAR(30),
    `FullPinYin` VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;

CREATE TABLE If Not Exists `funds_today` (
    `FundCode` VARCHAR(30),
    `Date` VARCHAR(30),
    `PriceToday` FLOAT,
    `PriceAllDay` FLOAT,
    `RangeToday` VARCHAR(30),
    `BuyStatus` VARCHAR(30),
    `SellStatus` VARCHAR(30),
    `RankToday` INT,
    PRIMARY KEY(FundCode, Date)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;

CREATE TABLE If Not Exists `funds_hybird` (
    `FundCode` VARCHAR(30),
    `Date` VARCHAR(30),
    `PriceToday` FLOAT,
    `PriceAllDay` FLOAT,
    `RangeToday` VARCHAR(30),
    `BuyStatus` VARCHAR(30),
    `SellStatus` VARCHAR(30),
    `RankToday` INT,
    PRIMARY KEY(FundCode, Date)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;


CREATE TABLE If Not Exists `funds_stock` (
    `FundCode` VARCHAR(30),
    `Date` VARCHAR(30),
    `PriceToday` FLOAT,
    `PriceAllDay` FLOAT,
    `RangeToday` VARCHAR(30),
    `BuyStatus` VARCHAR(30),
    `SellStatus` VARCHAR(30),
    `RankToday` INT,
    PRIMARY KEY(FundCode, Date)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;


CREATE TABLE If Not Exists `funds_bond` (
    `FundCode` VARCHAR(30),
    `Date` VARCHAR(30),
    `PriceToday` FLOAT,
    `PriceAllDay` FLOAT,
    `RangeToday` VARCHAR(30),
    `BuyStatus` VARCHAR(30),
    `SellStatus` VARCHAR(30),
    `RankToday` INT,
    PRIMARY KEY(FundCode, Date)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;

CREATE TABLE If Not Exists `funds_bond_dingkai` (
    `FundCode` VARCHAR(30),
    `Date` VARCHAR(30),
    `PriceToday` FLOAT,
    `PriceAllDay` FLOAT,
    `RangeToday` VARCHAR(30),
    `BuyStatus` VARCHAR(30),
    `SellStatus` VARCHAR(30),
    `RankToday` INT,
    PRIMARY KEY(FundCode, Date)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;

CREATE TABLE If Not Exists `funds_feeder` (
    `FundCode` VARCHAR(30),
    `Date` VARCHAR(30),
    `PriceToday` FLOAT,
    `PriceAllDay` FLOAT,
    `RangeToday` VARCHAR(30),
    `BuyStatus` VARCHAR(30),
    `SellStatus` VARCHAR(30),
    `RankToday` INT,
    PRIMARY KEY(FundCode, Date)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;

CREATE TABLE If Not Exists `funds_index` (
    `FundCode` VARCHAR(30),
    `Date` VARCHAR(30),
    `PriceToday` FLOAT,
    `PriceAllDay` FLOAT,
    `RangeToday` VARCHAR(30),
    `BuyStatus` VARCHAR(30),
    `SellStatus` VARCHAR(30),
    `RankToday` INT,
    PRIMARY KEY(FundCode, Date)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;

CREATE TABLE If Not Exists `funds_tiered_leveraged` (
    `FundCode` VARCHAR(30),
    `Date` VARCHAR(30),
    `PriceToday` FLOAT,
    `PriceAllDay` FLOAT,
    `RangeToday` VARCHAR(30),
    `BuyStatus` VARCHAR(30),
    `SellStatus` VARCHAR(30),
    `RankToday` INT,
    PRIMARY KEY(FundCode, Date)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;

CREATE TABLE If Not Exists `funds_qdii` (
    `FundCode` VARCHAR(30),
    `Date` VARCHAR(30),
    `PriceToday` FLOAT,
    `PriceAllDay` FLOAT,
    `RangeToday` VARCHAR(30),
    `BuyStatus` VARCHAR(30),
    `SellStatus` VARCHAR(30),
    `RankToday` INT,
    PRIMARY KEY(FundCode, Date)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;

CREATE TABLE If Not Exists `funds_range_period` (
    `FundCode` VARCHAR(30) PRIMARY KEY,
    `FullName` VARCHAR(30),
    `MaxPrice` FLOAT,
    `Date` VARCHAR(30),
    `RangePeriod` FLOAT,
    `BuyRange` FLOAT
) ENGINE=InnoDB DEFAULT CHARSET=gbk;


CREATE TABLE If Not Exists `funds_manager` (
    `Id` VARCHAR(30),
    `Name` VARCHAR(30),
    `CompanyId` VARCHAR(30),
    `CompanyName` VARCHAR(30),
    `Funds` VARCHAR(600),
    `FundNames` VARCHAR(600),
    PRIMARY KEY(Id)
) ENGINE=InnoDB DEFAULT CHARSET=gbk;