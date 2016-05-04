Use ANS;

SELECT * FROM BrowserEvents;

SELECT * FROM UserEventStore WHERE EventId = 2;

UPDATE UserEventStore SET PostId = 33997507;
#Query to get over all time spent by user
SELECT UserId, SUM(Duration) FROM UserEventStore WHERE EventId = 2 GROUP BY UserId;

SELECT * FROM PostTopicMap WHERE PostId = 33997507;
#Query to get topicwise time spent by user
SELECT DISTINCT P.TopicId, T.Name,U.UserId, U.PostId, SUM(Duration) FROM PostTopicMap P JOIN UserEventStore U ON P.PostId = U.PostId 
JOIN Topics T ON P.TopicId = T.Id
WHERE U.EventId = 2 AND U.UserId = 1 GROUP BY P.TopicId, U.UserId, T.Name, U.PostId;

SELECT SUM(Res.TimeDuration) FROM ((SELECT DISTINCT P.TopicId, T.Name,U.UserId, U.PostId, SUM(Duration) AS TimeDuration FROM PostTopicMap P JOIN UserEventStore U ON P.PostId = U.PostId 
JOIN Topics T ON P.TopicId = T.Id
WHERE U.EventId = 2 AND U.UserId = 1 GROUP BY P.TopicId, U.UserId, T.Name, U.PostId) AS Res);

SELECT DISTINCT P.TopicId, T.Name,U.UserId, SUM(Duration) FROM PostTopicMap P JOIN UserEventStore U ON P.PostId = U.PostId 
JOIN Topics T ON P.TopicId = T.Id
WHERE U.EventId = 2 AND U.UserId = 1 GROUP BY P.TopicId, U.UserId, T.Name;


SELECT DISTINCT P.TopicId, U.PostId, SUM(U.Duration) FROM PostTopicMap P JOIN UserEventStore U ON
P.PostId = U.PostId WHERE U.EventId = 2 AND U.UserId = 1 GROUP BY P.TopicId, U.PostId; 

SELECT * FROM PostTopicMap WHERE TopicId = 9;

SELECT * FROM Posts WHERE PostTypeId = 1 LIMIT 10;

27746536
31287528
27736168
27767577
27737358
34435981
29260919
27735088
27737183

INSERT INTO UserEventStore (UserDisplayName, UserId, EventId, StartTime, Endtime, PostId, Duration, PostTypeId, ActionCount)
VALUES
('jayaprakash', 1, 2, now(), now(), 27746536, 12, 1, null),
('jayaprakash', 1, 2, now(), now(), 31287528, 111, 1, null),
('jayaprakash', 1, 2, now(), now(), 27736168, 13, 1, null),
('jayaprakash', 1, 2, now(), now(), 27736168, 14, 1, null),
('jayaprakash', 1, 2, now(), now(), 27746536, 19, 1, null),
('jayaprakash', 1, 2, now(), now(), 27767577, 100, 1, null),
('jayaprakash', 1, 2, now(), now(), 34435981, 12, 1, null),
('jayaprakash', 1, 2, now(), now(), 34435981, 110, 1, null),
('jayaprakash', 1, 2, now(), now(), 27737358, 100, 1, null),
('jayaprakash', 1, 2, now(), now(), 27737358, 101, 1, null),
('jayaprakash', 1, 2, now(), now(), 27767577, 102, 1, null),
('jayaprakash', 1, 2, now(), now(), 34435981, 30, 1, null),
('jayaprakash', 1, 2, now(), now(), 34435981, 50, 1, null),
('jayaprakash', 1, 2, now(), now(), 29260919, 90, 1, null),
('jayaprakash', 1, 2, now(), now(), 29260919, 10, 1, null),
('jayaprakash', 1, 2, now(), now(), 27735088, 10, 1, null),
('jayaprakash', 1, 2, now(), now(), 27735088, 60, 1, null),
('jayaprakash', 1, 2, now(), now(), 27737183, 10, 1, null),
('jayaprakash', 1, 2, now(), now(), 27737183, 96, 1, null);

#Questions
SELECT M.TopicId, Count(*) AS Count FROM Posts P JOIN PostTopicMap M ON P.Id = M.PostId
WHERE P.OwnerUserID = 192801 AND P.PostTypeId = 1 GROUP BY M.TopicId;

#Answers
SELECT M.TopicId, Count(*) AS Count FROM Posts P JOIN PostTopicMap M ON P.ParentId = M.PostId
WHERE P.OwnerUserID = 12860 AND P.PostTypeId = 2 GROUP BY M.TopicId;


SELECT M.TopicId, COUNT(*) FROM Comments C JOIN PostTopicMap M ON C.PostId = M.PostId 
WHERE C.UserId =  1876620  GROUP BY M.TopicId;

#Question comments
SELECT M.TopicId, COUNT(*) FROM Comments C JOIN Posts P ON P.Id = C.PostId 
JOIN PostTopicMap M ON P.Id = M.PostId 
WHERE C.UserId =  2526083  GROUP BY M.TopicId;


SELECT SUM(Res.Counts) FROM ((SELECT M.TopicId, COUNT(*) AS Counts FROM Comments C JOIN Posts P ON P.Id = C.PostId 
JOIN PostTopicMap M ON P.Id = M.PostId 
WHERE C.UserId =  2526083  GROUP BY M.TopicId) AS Res);

#Answer Comments
SELECT M.TopicId, COUNT(*) FROM Comments C JOIN Posts P ON C.PostId = P.Id JOIN 
PostTopicMap M ON P.ParentId = M.PostId
WHERE C.UserId = 2526083 AND P.PostTypeId = 2 GROUP BY M.TopicId;

SELECT PostTypeId,OwnerUserId, COUNT(*) FROM Posts WHERE PostTypeId = 1 GROUP BY PostTypeId, OwnerUserId;

SELECT * FROM PostTopicMap WHERE PostId = 31041740;

############################
#Questions
(SELECT M.TopicId, Count(*) FROM Posts P JOIN PostTopicMap M ON P.Id = M.PostId
WHERE P.OwnerUserID = 192801 AND P.PostTypeId = 1 GROUP BY M.TopicId) AS Questions
JOIN Answers ON Questions.TopicId = Answers.TopicId
#Answers
(SELECT P.ParentId, M.TopicId, Count(*) FROM Posts P JOIN PostTopicMap M ON P.ParentId = M.PostId
WHERE P.OwnerUserID = 12860 AND P.PostTypeId = 2 GROUP BY M.TopicId, 
P.ParentId ORDER BY P.ParentId) AS Answers

#Question comments
(SELECT M.TopicId, COUNT(*) FROM Comments C JOIN Posts P ON P.Id = C.PostId 
JOIN PostTopicMap M ON P.Id = M.PostId 
WHERE C.UserId =  2526083  GROUP BY M.TopicId) AS QComments

#Answer Comments
(SELECT M.TopicId, COUNT(*) FROM Comments C JOIN Posts P ON C.PostId = P.Id JOIN 
PostTopicMap M ON P.ParentId = M.PostId
WHERE C.UserId = 2526083 AND P.PostTypeId = 2 GROUP BY M.TopicId) AS AComments

####

SELECT * FROM Topics;

SELECT * FROM Users;
INSERT INTO Users
(Id, DisplayName)
VALUES (3825558, '3825558');

SELECT OwnerUserId, COUNT(*) FROM Posts GROUP BY OwnerUserId LIMIT 100, 100;

UPDATE Posts SET Usefulness = 0;

SELECT P.Id, P.Title, P.ViewCount, P.OwnerUserId, P.OwnerDisplayName, P.FavouriteCount, P.Tags, 
            P.AnswerCount, P.CreationDate, P.Usefulness from Posts as P where P.PostTypeId = 1 
            AND P.Id IN (SELECT Ps.ParentId FROM Posts as Ps WHERE Ps.PostTypeId = 2 AND Ps.OwnerUserId = 192801) LIMIT 1,10;
9204
SELECT COUNT(*) FROM Comments WHERE UserId = 9204;
SELECT * FROM Posts WHERE OwnerUserId = 2526083 AND PostTypeId = 2;


SELECT P.Id AS Id, P.PostTypeId AS PostTypeId, P.Title AS Title, 
P.CreationDate AS CreationDate, P.OwnerUserId AS OwnerUserId, 
P.AcceptedAnswerId AS AcceptedAnswerId, U.DisplayName AS OwnerDisplayName
FROM Posts P JOIN Users U
ON P.OwnerUserId = U.Id
WHERE P.Id =  32482636; 

SELECT * FROM Posts WHERE Id = 32482636;


#########
SELECT P.Id AS Id, P.PostTypeId AS PostTypeId, P.Title AS Title, P.Body AS Body, 
P.CreationDate AS CreationDate, P.OwnerUserId AS OwnerUserId, P.Score AS Score,
P.AcceptedAnswerId AS AcceptedAnswerId, U.DisplayName AS OwnerDisplayName
FROM Posts P JOIN Users U
ON P.OwnerUserId = U.Id
WHERE P.Id =  32482636;

SELECT COUNT(*) AS Count FROM Bookmarks WHERE UserId = 1 AND PostId = 27727912
AND isDeleted = 0;


SELECT * FROM Users WHERE DisplayName = 'Weber';

SELECT * FROM Comments where UserId = 9204;

SELECT * FROM Posts WHERE OwnerUserId = 9204;

SELECT P.Id, P.Title, P.ViewCount, P.OwnerUserId, P.OwnerDisplayName, P.FavouriteCount, P.Tags,
            P.AnswerCount, P.CreationDate, P.Usefulness from Posts as P where P.PostTypeId = 1 and P.OwnerUserId = 9204;

SELECT * FROM Posts WHERE Id = 28815982;

SELECT P.Id AS Id, P.PostTypeId AS PostTypeId, P.Title AS Title, P.Body AS Body,
				 	 P.CreationDate AS CreationDate, P.OwnerUserId AS OwnerUserId, P.Score AS Score, P.Tags AS Tags,
					 P.AcceptedAnswerId AS AcceptedAnswerId, U.DisplayName AS OwnerDisplayName, P.AnswerCount AS AnswerCount
					 FROM Posts P JOIN Users U
					 ON P.OwnerUserId = U.Id
					 WHERE P.Id =  29203233;
                     
SELECT * FROM Posts WHERE Id = 29203233;

SELECT * FROM FollowDetails;

