use ans;

#Master-Table for storing the browser events
CREATE TABLE BrowserEvents(
Id INT,
EventName VARCHAR(300)
);

ALTER TABLE BrowserEvents ADD CONSTRAINT PK_ID PRIMARY KEY (Id);

ALTER TABLE BrowserEvents MODIFY Id  INT NOT NULL AUTO_INCREMENT;

#DROP TABLE UserEventStore;

CREATE TABLE UserEventStore(
Id INT,
UserDisplayName VARCHAR(100),
UserId INT,
EventId INT NOT NULL,
StartTime DATETIME,
EndTime DATETIME,
PostId INT NULL,
Duration INT NULL,
PostTypeId INT,
ActionCount INT
);

ALTER TABLE UserEventStore ADD CONSTRAINT PK_ID PRIMARY KEY (Id);

ALTER TABLE UserEventStore MODIFY Id  INT NOT NULL AUTO_INCREMENT;

ALTER TABLE UserEventStore ADD CONSTRAINT FK_EventId_UserEventStore FOREIGN KEY (EventId)
REFERENCES BrowserEvents (Id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE UserEventStore ADD CONSTRAINT FK_PostId_UserEventStore FOREIGN KEY (PostId)
REFERENCES Posts (Id) ON UPDATE CASCADE ON DELETE CASCADE;

INSERT INTO BrowserEvents (EventName) VALUES ('PageClick'),('TimeSpent'),('TextSelection');

CREATE TABLE UserRatingsScore(
Id INT,
UserId INT,
PostId INT,
Rating INT,
CreationDate DATETIME
);

ALTER TABLE UserRatingsScore ADD CONSTRAINT PK_ID_UserRatingsScore PRIMARY KEY (Id);
#ALTER TABLE UserRatingsScore ADD CONSTRAINT FK_UserId_UserRatingsScore FOREIGN KEY (UserId)
#REFERENCES Users (Id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE UserRatingsScore ADD CONSTRAINT FK_PostId_UserRatingsScore FOREIGN KEY (PostId)
REFERENCES Posts (Id) ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE UserRatingsScore MODIFY Id  INT NOT NULL AUTO_INCREMENT;


#select count(*) from Posts where PostTypeId = 1 and MATCH(Body, Title) against ('+*iterator* -php -android' in boolean mode) or MATCH(Body, Title) against ('+loop* -php -android' in boolean mode) or tags like '%iterator%' or tags like 'loop%';


#select count(*) from Posts where PostTypeId = 1 and MATCH(Body, Title) against ('+*thread* -php -android' in boolean mode) or MATCH(Body, Title) against ('+synchronize* -php -android' in boolean mode) or tags like '%thread%' or tags like 'synchronize%';