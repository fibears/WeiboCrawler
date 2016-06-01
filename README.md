# 新浪微博爬虫程序

## 目标

爬取新浪微博数据。

## 工具
- Python2.7
- scrapy爬虫框架
- selenium
- phantomjs

未完待续...

@Fibears

## MySQL

```mysql
# Create Database
create database PaperData;
use `PaperData`;
CREATE TABLE `Content` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `Type` varchar(30) DEFAULT NULL,
  `ContentId` varchar(200) NOT NULL DEFAULT '',
  `uid` varchar(30) DEFAULT NULL,
  `Name` varchar(30) DEFAULT NULL,
  `Content` mediumtext,
  `Repost` varchar(30) NOT NULL DEFAULT '0',
  `Comment` varchar(30) NOT NULL DEFAULT '0',
  `Like` varchar(30) NOT NULL DEFAULT '0',
  `PostTime` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `ContentId_index` (`ContentId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `CommentInformation` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `Type` varchar(30) DEFAULT NULL,
  `CommentId` varchar(200) NOT NULL DEFAULT '',
  `uid` varchar(30) DEFAULT NULL,
  `Name` varchar(30) DEFAULT NULL,
  `Content` mediumtext,
  `PostTime` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `CommentId_index` (`CommentId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `UserInformation` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `uid` varchar(30) DEFAULT NULL,
  `Name` varchar(30) DEFAULT NULL,
  `TweetsNum` varchar(30) NOT NULL DEFAULT '0',
  `FansNum` varchar(30) NOT NULL DEFAULT '0',
  `FollowersNum` varchar(30) NOT NULL DEFAULT '0',
  `CrawlFollowers` varchar(30) NOT NULL DEFAULT '0',
  `Follower` longtext,
  PRIMARY KEY (`id`),
  KEY `uid_index` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# Extract Data
select *  from UserInformation into outfile '/tmp/UserInformation.csv' fields terminated by ','optionally enclosed by '"' escaped by '"' lines terminated by '\r\n';
```