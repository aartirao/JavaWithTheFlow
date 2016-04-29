Create DATABASE ANS;

USE ANS;

CREATE TABLE Comments (
Id INT,
PostId INT,
Score INT,
Text VARCHAR(2000),
CreationDate DATETIME,
UserDisplayName VARCHAR(100),
UserId INT);


CREATE TABLE Posts(
Id INT,
PostTypeId INT,
AcceptedAnswerId INT,
ParentId INT,
CreationDate DATETIME,
DeletionDate DATETIME,
Score INT,
ViewCount INT,
Body TEXT,
OwnerUserId INT,
OwnerDisplayName VARCHAR(100),
LastEditorUserId INT,
LastedEditorDisplayName VARCHAR(100),
LastEditDate DATETIME,
LastActivityDate DATETIME,
Title VARCHAR(400),
Tags VARCHAR(200),
AnswerCount INT,
CommentCount INT,
FavouriteCount INT,
ClosedDate DATETIME,
Usefulness INT
);

CREATE TABLE Users(
Id INT,
Reputation INT,
CreationDate DATETIME,
DisplayName VARCHAR(100),
LastAccessDate DATETIME,
Location VARCHAR(100),
AboutMe VARCHAR(500),
Views INT,
UpVotes INT,
DownVotes INT,
AccountId INT,
Age INT,
Password VARCHAR(20)
);

CREATE TABLE Badges(
Id INT,
UserId INT,
Name VARCHAR(200),
Date DATETIME,
Class INT,
TagBased BOOLEAN
);

CREATE TABLE PostTags(
PostId  INT,
TagId INT
);

CREATE TABLE Tags(
Id  INT,
TagName  VARCHAR(200),
Count  INT
);


CREATE TABLE TagSynonyms(
Id  INT,
SourceTagName  VARCHAR(200),
TargetTagName  VARCHAR(200),
CreationDate  DATETIME,
OwnerUserId  INT,
AutoRenameCount  INT,
LastAutoRename  INT,
Score  INT);

CREATE TABLE Votes(
Id INT,
PostId  INT,
VoteTypeId  INT,
UserId  INT,
CreationDate  DATETIME);

CREATE TABLE UserInfo(
Id  INT,
UserId  INT,
Interests  VARCHAR(300));


CREATE TABLE FollowDetails(
Id  INT,
UserId  INT,
FollowingUserId  INT,
IsDeleted  BOOLEAN
);


CREATE TABLE UserExpertise(
Id  INT,
UserId  INT,
Topics  VARCHAR(200),
Level  INT);


create table `Topics` (
	`Id` int(11) DEFAULT NULL,
	`Name` VARCHAR(1000) DEFAULT NULL
);

create table `TopicKeywordMap` (
	`id` int(11) DEFAULT NULL,
	`TopicId` int(11) DEFAULT NULL,
	`SearchCond` varchar(1000) DEFAULT NULL
);

create table `PostTopicMap` (
	`Id` int(11) DEFAULT NULL,
	`PostId` int(11) DEFAULT NULL,
	`TopicId` int(11) DEFAULT NULL
);

ALTER TABLE Users ADD CONSTRAINT PK_ID PRIMARY KEY (Id);

create table Bookmarks (
Id INT,
UserId INT,
PostId INT,
CreationDate DATETIME,
IsDeleted INT(1));

ALTER TABLE Bookmarks ADD CONSTRAINT PK_ID PRIMARY KEY (Id);
ALTER TABLE Bookmarks MODIFY Id INT NOT NULL AUTO_INCREMENT;
ALTER TABLE Bookmarks AUTO_INCREMENT = 1;

#ALTER TABLE Bookmarks ADD CONSTRAINT FK_POSTID_Bookmarks FOREIGN KEY (PostId) 
#REFERENCES Posts (Id) ON UPDATE CASCADE ON DELETE CASCADE;


#ALTER TABLE Bookmarks ADD CONSTRAINT FK_USERID_Bookmarks FOREIGN KEY (UserId) 
#REFERENCES Users (Id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE Bookmarks ADD CONSTRAINT UK_ID UNIQUE KEY (PostId, UserId);

create table UserInterests (
Id INT,
UserId INT,
TopicId INT,
Weight INT);

ALTER TABLE UserInterests ADD CONSTRAINT PK_ID PRIMARY KEY (Id);
ALTER TABLE UserInterests MODIFY Id INT NOT NULL AUTO_INCREMENT;
ALTER TABLE UserInterests AUTO_INCREMENT = 1;
#ALTER TABLE UserInterests ADD CONSTRAINT FK_USERID_UserInterests FOREIGN KEY (UserId) 
#REFERENCES Users (Id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE Topics ADD CONSTRAINT PK_ID PRIMARY KEY (Id);

#ALTER TABLE UserInterests ADD CONSTRAINT FK_TOPICID_UserInterests FOREIGN KEY (TopicId) 
#REFERENCES Topics (Id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE UserInterests ADD CONSTRAINT UK_ID UNIQUE KEY (UserId, TopicId);

create table TopicConceptMap (
TopicIdFrom INT,
TopicIdTo INT);

ALTER TABLE TopicConceptMap ADD CONSTRAINT UK_ID UNIQUE KEY (TopicIdFrom, TopicIdTo);