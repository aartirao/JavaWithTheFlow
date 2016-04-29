USE aweb;

#Posts table

ALTER TABLE Posts ADD CONSTRAINT PK_ID PRIMARY KEY (Id);

ALTER TABLE Posts MODIFY Id INT NOT NULL AUTO_INCREMENT;

ALTER TABLE Posts AUTO_INCREMENT=36524876;

#Comments Table
ALTER TABLE Comments ADD CONSTRAINT PK_ID PRIMARY KEY (Id);

ALTER TABLE Comments MODIFY Id INT NOT NULL AUTO_INCREMENT;
ALTER TABLE Comments AUTO_INCREMENT = 660656166;
DELETE FROM Comments WHERE PostId NOT IN (SELECT Id FROM Posts);
#Foriegn Key between posts and comments
ALTER TABLE Comments ADD CONSTRAINT FK_POSTID_Comments FOREIGN KEY (PostId)
REFERENCES Posts (Id) ON UPDATE CASCADE ON DELETE CASCADE;

#Topics table
ALTER TABLE Topics ADD CONSTRAINT PK_ID PRIMARY KEY (Id);
ALTER TABLE Topics MODIFY Id  INT NOT NULL AUTO_INCREMENT;

ALTER TABLE Topics AUTO_INCREMENT = 17;

#TopicKeywordMap table
ALTER TABLE TopicKeywordMap ADD CONSTRAINT PK_ID PRIMARY KEY (Id);
ALTER TABLE TopicKeywordMap MODIFY Id  INT NOT NULL AUTO_INCREMENT;

ALTER TABLE TopicKeywordMap ADD CONSTRAINT FK_TOPICID FOREIGN KEY (TopicId)
REFERENCES Topics (Id) ON UPDATE CASCADE ON DELETE CASCADE;

#PostTopicMap table
ALTER TABLE PostTopicMap ADD CONSTRAINT PK_ID PRIMARY KEY (Id);
ALTER TABLE PostTopicMap MODIFY Id  INT NOT NULL AUTO_INCREMENT;
ALTER TABLE PostTopicMap AUTO_INCREMENT = 140465;

ALTER TABLE PostTopicMap ADD CONSTRAINT FK_TOPICID_PostTopicMap FOREIGN KEY (TopicId)
REFERENCES Topics (Id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE PostTopicMap ADD CONSTRAINT FK_POSTID_PostTopicMap FOREIGN KEY (PostId)
REFERENCES Posts (Id) ON UPDATE CASCADE ON DELETE CASCADE;

#Votes table
ALTER TABLE Votes ADD CONSTRAINT PK_Id_Votes PRIMARY KEY (Id);
ALTER TABLE Votes MODIFY Id  INT NOT NULL AUTO_INCREMENT;
ALTER TABLE Votes AUTO_INCREMENT = 111489335;

#FollowDetails
ALTER TABLE FollowDetails ADD CONSTRAINT PK_Id_FollowDetails PRIMARY KEY (Id);
ALTER TABLE FollowDetails MODIFY Id  INT NOT NULL AUTO_INCREMENT;
#Fulltext search

ALTER TABLE Posts ADD FULLTEXT Body_Index(Body);
ALTER TABLE Posts ADD FULLTEXT Body_Title_Index(Body, Title);

ALTER TABLE Posts ADD Column Usefulness INT;


ALTER TABLE Users MODIFY Id INT NOT NULL AUTO_INCREMENT;

ALTER TABLE Users AUTO_INCREMENT = 1;

#SELECT DISTINCT PostId FROM Comments;

#SELECT * FROM Posts WHERE Id IN (
#SELECT PostId FROM Comments WHERE PostId NOT IN (SELECT Id FROM Posts));

#SELECT PostId FROM Comments WHERE PostId NOT IN (SELECT Id FROM Posts);
#SELECT COUNT(*) FROM Comments;
#SELECT COUNT(*) FROM Comments WHERE PostId IN 
#(SELECT PostId FROM Comments WHERE PostId NOT IN (SELECT Id FROM Posts));
#DELETE FROM Comments WHERE PostId NOT IN (SELECT Id FROM Posts);
