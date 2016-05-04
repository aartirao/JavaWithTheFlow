import pymysql.cursors
import datetime
import traceback
import json
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('db.cfg')


connection = pymysql.connect(host=config.get('database','host'),
							 user=config.get('database','username'),
							 password=config.get('database','password'),
							 db = config.get('database','db'),
							 charset = 'utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

#Method to save answer
def saveAnswer(data):
	#data = request.json
	postTypeId = 2
	parentId = data["QuestionId"]
	creationDate = datetime.datetime.now()
	score = 0
	viewcount = 1
	body = data["Body"]
	displayname = data["DisplayName"]
	#insert this into database in Posts table
	try:
		#Get user id for the diplayname
		with connection.cursor() as cursor:
			sql = "SELECT `Id` FROM `Users` WHERE `DisplayName` = %s"
			cursor.execute(sql, (displayname))
			userId = cursor.fetchone()
			
		#save the answer in database
		with connection.cursor() as cursor:
			sql = """INSERT INTO `posts` (
				`PostTypeId`,
				`AcceptedAnswerId`,
				`ParentId`,
				`CreationDate`,
				`DeletionDate`,
				`Score`,
				`ViewCount`,
				`Body`,
				`OwnerUserId`,
				`OwnerDisplayName`,
				`LastEditorUserId`,
				`LastedEditorDisplayName`,
				`LastEditDate`,
				`LastActivityDate`,
				`Title`,
				`Tags`,
				`AnswerCount`,
				`CommentCount`,
				`FavouriteCount`,
				`ClosedDate`) VALUES (%s, %s, %s, %s, %s,
				%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
				%s, %s, %s)"""
				
			cursor.execute(sql, (postTypeId, None, parentId, creationDate, None, 
			score, viewcount, body, userId["Id"], displayname, None, None, None, None, None, 
			None, None, 0, None, None))
			
			newRowId = cursor.lastrowid

		#Update the answer count in database for the question
		with connection.cursor() as cursor:
			sql = """UPDATE `Posts` SET 
				`AnswerCount` = `AnswerCount` + 1
				WHERE `Id` = %s"""
			cursor.execute(sql, (parentId))
		connection.commit()
		return newRowId
	except Exception, e:
		print traceback.print_exc()
		return -1

#Method to save comments
def saveComment(data):
	postId = data["PostId"]
	score = 0
	text = data["Text"]
	creationDate = datetime.datetime.now()
	displayname = data["DisplayName"]
	try:
		#Select the userid for the current user
		with connection.cursor() as cursor:
			sql = "SELECT `Id` FROM `Users` WHERE `DisplayName` = %s"
			cursor.execute(sql, (displayname))
			userId = cursor.fetchone()

		#Insert the new comment into database
		with connection.cursor() as cursor:
			sql = """INSERT INTO `Comments` (
				`PostId`,
				`Score`,
				`Text`,
				`CreationDate`,
				`UserDisplayName`,
				`UserId`) VALUES (%s, %s, %s, %s, %s, %s)"""
			cursor.execute(sql, (postId, score, text, creationDate, 
				displayname, userId["Id"]))
			#print("id="+str(cursor.lastrowid))
		#update comment count for the post
		with connection.cursor() as cursor:
			sql = """UPDATE `Posts` SET 
				`CommentCount` = `CommentCount` + 1
				WHERE `Id` = %s"""
			cursor.execute(sql, (postId))
		connection.commit()
		return 1
	except Exception, e:
		print traceback.print_exc()
		return -1
		
#Method to store the user rating for an answer
def saveUserRating(data):
	postId = data["PostId"]
	creationDate = datetime.datetime.now()
	userId = data["UserId"]
	ratingScore = data["RatingScore"]
	ret = -1
	try:
		with connection.cursor() as cursor:
			sql = "CALL `sp_UpdateUserRatingScore`(%s, %s, %s)"
			cursor.execute(sql, (postId, userId, ratingScore))
			ret = cursor.fetchone()
			ret = 1
		connection.commit()
		return ret
	except Exception, e:
		print traceback.print_exc()
		return -1

	

#Method for adding new question
def addQuestion(data):
	postTypeId = 1
	acceptedAnswerId = -1
	parentId = None
	creationDate = datetime.datetime.now()
	score = 0
	deletionDate = None
	viewcount = 1
	body = data["Body"]
	displayname = data["DisplayName"]
	title = data["Title"]
	tags = data["Tags"] #Do we need to update it automatically?
	answerCount = 0
	commentCount = 0
	favouriteCount = 0
	tagstobeEntered = ""
	if tags != "":
		temp = tags.split(",")
		for item in temp:
			tagstobeEntered = tagstobeEntered + "<" + item + ">"
		
	try:
		#Get user id for the diplayname
		with connection.cursor() as cursor:
			sql = "SELECT `Id` FROM `Users` WHERE `DisplayName` = %s"
			cursor.execute(sql, (displayname))
			userId = cursor.fetchone()
		#save the question in database
		with connection.cursor() as cursor:
			sql = """INSERT INTO `posts` (
				`PostTypeId`,
				`AcceptedAnswerId`,
				`ParentId`,
				`CreationDate`,
				`DeletionDate`,
				`Score`,
				`ViewCount`,
				`Body`,
				`OwnerUserId`,
				`OwnerDisplayName`,
				`LastEditorUserId`,
				`LastedEditorDisplayName`,
				`LastEditDate`,
				`LastActivityDate`,
				`Title`,
				`Tags`,
				`AnswerCount`,
				`CommentCount`,
				`FavouriteCount`,
				`ClosedDate`) VALUES (%s, %s, %s, %s, %s,
				%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
				%s, %s, %s)"""
				
			cursor.execute(sql, (postTypeId, acceptedAnswerId, 
				parentId, creationDate, None, 
				score, viewcount, body, userId["Id"], 
				displayname, None, None, None, None, title, 
				tagstobeEntered, answerCount, 0, 0, None))

		connection.commit()
		return 1
	except Exception, e:
		print traceback.print_exc()
		return -1

#Method to retrieve comments
def getComments(parentId, uId):
	comments = []
	comment = {}
	try:
		with connection.cursor() as cursor:
			sql = """SELECT C.Id AS Id, C.CreationDate AS CreationDate, C.Text AS Text, 
					 C.UserId AS UserId, U.DisplayName AS UserDisplayName
					 FROM Comments C JOIN Users U
					 ON C.UserId = U.Id
					 WHERE C.PostId = %s"""
			rowCount = cursor.execute(sql, (parentId))
			if rowCount > 0:
				results = cursor.fetchall()
				for row  in results:					
					commentId = row[u'Id']
					commentedUser = row[u'UserDisplayName']
					commentedTime = str(row[u'CreationDate'])
					commentText = row[u'Text']
					commentedUserId = row[u'UserId']
					userUrl = "/profile?uId="+str(commentedUserId)+"&cId="+str(uId)
					comment = {
						"commentId": commentId,
						"commentedUser": commentedUser,
						"commentedTime": commentedTime,
						"commentText": commentText,
						"userUrl": userUrl 
					}
					comments.append(comment)

		connection.commit()
		return comments
	except Exception, e:
		print traceback.print_exc()
		return -1
	
#Method to get current user rating of a post
def getCurrentUserRating(userId, postId) :
	rating = 0
	try:	
		#Select the rating for a post given by a user
		with connection.cursor() as cursor:
			sql = "SELECT `Rating` FROM `UserRatingsScore` WHERE `PostId` = %s and `UserId` = %s"
			rowCount = cursor.execute(sql, (postId, userId))
			if rowCount > 0:
				result = cursor.fetchone()
				rating = result[u'Rating']

	except Exception, e:
		print traceback.print_exc()

	return rating


#Method to retrieve answers along with comments
def getAnswers(parentId, userId):
	answers = []
	comments = []
	temp = {}
	userRating = 0

	try:
		#Select the answer with the particular id
		with connection.cursor() as cursor:
			sql = """SELECT P.Id AS Id, P.PostTypeId AS PostTypeId, P.Title AS Title, P.Body AS Body, 
					 P.CreationDate AS CreationDate, P.OwnerUserId AS OwnerUserId, P.Score AS Score,
					 P.AcceptedAnswerId AS AcceptedAnswerId, U.DisplayName AS OwnerDisplayName
					 FROM Posts P JOIN Users U
					 ON P.OwnerUserId = U.Id
					 WHERE P.ParentId =  %s"""
			rowCount = cursor.execute(sql, (parentId))
			if rowCount > 0:
				results = cursor.fetchall()
				for row in results:					
					postId = row[u'Id']				
					postTypeId = row[u'PostTypeId']
					postText =  row[u'Body']
					answeredByUserName = row[u'OwnerDisplayName']
					answeredByUserId = row[u'OwnerUserId']
					answeredUserProfile = "/profile?uId="+str(answeredByUserId)+"&cId="+str(userId)
					answeredDate = str(row[u'CreationDate'])
					isAcceptedAnswer = "#"
					usefulness = "#"
					score = row[u'Score']
					upvotes = "#"
					downvotes = "#"

					ratings = getUserRatings(postId)

					if(userId != 0):
						userRating = getCurrentUserRating(userId, postId)
				
					answer = {
						"postId": postId,
						"postTypeId": postTypeId,
						"postText": postText,
						"answeredbyUserName": answeredByUserName,
						"answeredbyUserId": answeredByUserId,
						"answeredUserProfile": answeredUserProfile,
						"answeredDate": answeredDate,
						"isAcceptedAnswer": isAcceptedAnswer,
						"usefulness": usefulness,
						"score": score,
						"upvotes": "#",
						"downvotes": "#",
						"excitedCount": ratings[0],
			            "happyCount": ratings[1],
			            "neutralCount": ratings[2],
			            "confusedCount": ratings[3],
			            "angryCount": ratings[4],
			            "currentUserRating": userRating
					}

					comments = getComments(postId, userId)
					temp = {"answer" : answer, "comments" : comments}
					answers.append(temp)

		return answers
	except Exception, e:
		print traceback.print_exc()
		return -1

#Method to get user ratings for a question   10 7 2 -3 -5
def getUserRatings(qId):

	count = []
	excitedCount = 0
	happyCount = 0
	neutralCount = 0
	confusedCount = 0
	angryCount = 0
	currentUserRating = 0

	try:
		#Get count of user ratings
		with connection.cursor() as cursor:
			sql = "select count(*) as counts, `Rating` from `UserRatingsScore` WHERE `PostId` = %s GROUP by `Rating`"
			rowCount = cursor.execute(sql, (qId))
			if rowCount > 0:
				results = cursor.fetchall()
				for row in results:
					if(row[u'Rating'] == 10):
						excitedCount = row[u'counts']
					elif(row[u'Rating'] == 7):
						happyCount = row[u'counts']
					elif(row[u'Rating'] == 2):
						neutralCount = row[u'counts']
					elif(row[u'Rating'] == -3):
						confusedCount = row[u'counts']
					elif(row[u'Rating'] == -5):
						angryCount = row[u'counts']

			count.extend((excitedCount, happyCount, neutralCount, confusedCount, angryCount,currentUserRating))
		
		connection.commit()
		return count

	except Exception, e:
		print traceback.print_exc()
		return -1


#Method to retrieve post details 
def getQuestion(data,user):
	qId = data
	uId = user
	question = {}
	try:
		#Select the question with the particular postId
		with connection.cursor() as cursor:
			sql = """SELECT P.Id AS Id, P.PostTypeId AS PostTypeId, P.Title AS Title, P.Body AS Body,
				 	 P.CreationDate AS CreationDate, P.OwnerUserId AS OwnerUserId, P.Score AS Score, P.Tags AS Tags,
					 P.AcceptedAnswerId AS AcceptedAnswerId, U.DisplayName AS OwnerDisplayName, P.AnswerCount AS AnswerCount
					 FROM Posts P JOIN Users U
					 ON P.OwnerUserId = U.Id
					 WHERE P.Id =  %s"""
			rowCount = cursor.execute(sql, (qId))
			if rowCount > 0:
				results = cursor.fetchall()
				sql = """SELECT COUNT(*) AS Count FROM Bookmarks WHERE UserId = %s AND PostId = %s
					 AND isDeleted = 0"""
				cursor.execute(sql,(uId, qId))
				bookmarkcount = cursor.fetchone()
				isbookmark = bookmarkcount["Count"]
				if isbookmark >= 1:
					isbookmark = 1
				for row in results:																
					postId = row[u'Id']
					postTypeId = row[u'PostTypeId']
					postTitle = row[u'Title']
					postText = row[u'Body']
					usefulness = "#"
					traffic = "#"
					upvotes = "#"
					downvotes = "#"
					score = row[u'Score']
					isFavorite = "#"
					tags = row[u'Tags']
					askedDate = str(row[u'CreationDate'])
					status = "#"
					askedByUserName = row[u'OwnerDisplayName']
					askedByUserId = row[u'OwnerUserId']
					askedUserProfile = "/profile?uId="+str(askedByUserId)+"&cId="+str(uId)
					noOfAnswers = row[u'AnswerCount']
					acceptedAnswerId = row[u'AcceptedAnswerId']
			
				
					question =  {
						"postId": postId,
						"postTypeId": postTypeId,
						"postTitle": postTitle,
						"postText": postText,
						"usefulness": usefulness,
						"traffic": traffic,
						"upvotes": upvotes,
						"downvotes": downvotes,
						"score": score,
						"isFavorite": isFavorite,
						"tags": tags,
						"askedDate": askedDate,
						"status": status,
						"askedbyUserName": askedByUserName,
						"askedbyUserId": askedByUserId,
						"askedUserProfile": askedUserProfile,
						"noOfAnswers": noOfAnswers,
						"acceptedAnswerId" : acceptedAnswerId,
						"isBookMarked" : isbookmark
	  				}

		comments = getComments(qId, uId)
		answers = getAnswers(qId,uId)
		final = {"question" : question, "comments" : comments, "answers" : answers}

		connection.commit()
		return final
	except Exception, e:
		print traceback.print_exc()
		return -1

#Method to return view counts for each topic
def getViewCount():
	data = []
	try:
		# Get all topics
		with connection.cursor() as cursor:
			sql = "SELECT * FROM `Topics`"
			rowCount = cursor.execute(sql)
			if rowCount > 0:
				results = cursor.fetchall()
				for row in results:
					# Get list of question ids under each topic
					topicSql = "SELECT `PostId` from `PostTopicMap` where `TopicId` = %s"
					topicRowCount = cursor.execute(topicSql, (row[u'Id']))					
					if(topicRowCount > 0):
						topicResults = cursor.fetchall()
						postIds = []
						for topicRow in topicResults:
							postIds.append(topicRow[u'PostId'])
						# Calculate sum of view counts
						viewCountSql = "SELECT sum(`ViewCount`) from `Posts` where `Id` in (%s)"
						# Some high tech execution #YOLO 
						in_p=', '.join(list(map(lambda x: '%s', postIds)))
						viewCountSql = viewCountSql % in_p
						viewCountRowCount = cursor.execute(viewCountSql, postIds)
						temp = {}
						temp["topicName"] = str(row[u'Name'])
						if(viewCountRowCount > 0):
							viewCountResults = cursor.fetchone()	
							temp["viewCount"] = str(viewCountResults[u'sum(`ViewCount`)'])
						else:
							temp["viewCount"] = '0'	
						data.append(temp)			
		return data
	except Exception, e:
		print traceback.print_exc()
		return -1	
	
def getRange(v1, v2, v3, x):
	if x in v3:
		return 3
	elif x in v2:
		return 2
	else:
		return 1
	
	
def getSortedQuestionListByTopic(topic, parameter, page):
	pageNum = (int(page)-1) * 10;
	data = {}
	try:
		# Get all questions by topic
		# order by P.ViewCount desc
		with connection.cursor() as cursor:
			sqlUsefulness = "SELECT P.Id, P.Title, P.ViewCount, P.OwnerUserId, P.OwnerDisplayName, P.FavouriteCount, P.Tags, \
			P.AnswerCount, P.CreationDate, P.Usefulness from Posts as P where P.PostTypeId = 1 and P.Id in (select PT.PostId from \
			Topics as T join PostTopicMap as PT on T.Name = %s and PT.TopicId = T.Id) ORDER BY Usefulness DESC LIMIT %s,10"
			
			sqlViewCount = "SELECT P.Id, P.Title, P.ViewCount, P.OwnerUserId, P.OwnerDisplayName, P.FavouriteCount, P.Tags, \
			P.AnswerCount, P.CreationDate, P.Usefulness from Posts as P where P.PostTypeId = 1 and P.Id in (select PT.PostId from \
			Topics as T join PostTopicMap as PT on T.Name = %s and PT.TopicId = T.Id) ORDER BY ViewCount DESC LIMIT %s,10"
			
			sql = sqlUsefulness if parameter == "Usefulness" else sqlViewCount
			rowCount = cursor.execute(sql, (topic, pageNum))	
			if rowCount > 0:
				results = cursor.fetchall()
				usefulnessCounts = []
				viewCounts = []
				for row in results:
					viewCounts.append(int(row[u'ViewCount']))
					usefulnessCounts.append(int(row[u'Usefulness']))
				viewCounts.sort()
				usefulnessCounts.sort()
				splitAt = rowCount / 3
				v1 = viewCounts[:splitAt]
				v2 = viewCounts[splitAt:splitAt*2]
				v3 = viewCounts[splitAt*2:]
				u1 = usefulnessCounts[:splitAt]
				u2 = usefulnessCounts[splitAt:splitAt*2]
				u3 = usefulnessCounts[splitAt*2:]
				
				for row in results:
					id = row[u'Id']
					sqlVup = "SELECT count(Id) as count from Votes where VoteTypeId = 2 and PostId = %s"
					sqlVdown = "SELECT count(Id) as count from Votes where VoteTypeId = 3 and PostId = %s"
					upCount = cursor.execute(sqlVup, (id))
					up = cursor.fetchone()
					downCount = cursor.execute(sqlVdown, (id))
					down = cursor.fetchone()
					row[u'CreationDate'] = str(row[u'CreationDate'])
					row[u'UpVotes'] = up[u'count']
					row[u'DownVotes'] = down[u'count']	
					row[u'ViewCountRank'] = getRange(v1, v2, v3, row[u'ViewCount'])
					row[u'UsefulnessRank'] = getRange(u1, u2, u3, row[u'Usefulness'])
				data = results
			return data		
	except Exception, e:
		print traceback.print_exc()
		return -1

def createBookmark(userId, postId):
	creationDate = datetime.datetime.now()	
	try :
		with connection.cursor() as cursor:
			sql = "SELECT UserId, PostId, IsDeleted from Bookmarks where UserId = %s and PostId = %s"
			rowCount = cursor.execute(sql, (userId, postId))
			
			if rowCount > 0:
				dele = 0
				result = cursor.fetchone()
				if result[u'IsDeleted'] == 1:
					dele = 0
				else:
					dele = 1
				sql = "UPDATE Bookmarks set IsDeleted = %s where UserId = %s and PostId = %s"
				cursor.execute(sql, (dele, userId, postId))
				connection.commit()
			else: 
				sql = "INSERT INTO Bookmarks (UserId, PostId, CreationDate, IsDeleted) values (%s, %s, %s, 0)"
				cursor.execute(sql, (userId, postId, creationDate))
				connection.commit()
		return 1
	except Exception, e:
		print traceback.print_exc()
		return -1
		
def getQuestionListByBookmark(user):
	data = {}
	try:
		# Get all questions by topic
		# order by P.ViewCount desc
		with connection.cursor() as cursor:
			sql = "SELECT P.Id, P.Title, P.ViewCount, P.OwnerUserId, P.OwnerDisplayName, P.FavouriteCount, P.Tags, \
				P.AnswerCount, P.CreationDate, P.Usefulness from Posts as P where P.PostTypeId = 1 and P.Id in \
				(SELECT PostId from Bookmarks where UserId = %s and IsDeleted = 0) LIMIT 10;"
			rowCount = cursor.execute(sql, (user))	
			if rowCount > 0:
				results = cursor.fetchall()
				sumViewCount = 0
				viewCounts = []
				usefulnessCounts = []
				for row in results:
					viewCounts.append(int(row[u'ViewCount']))
					usefulnessCounts.append(int(row[u'Usefulness']))
				viewCounts.sort()
				usefulnessCounts.sort();
				splitAt = rowCount / 3
				v1 = viewCounts[:splitAt]
				v2 = viewCounts[splitAt:splitAt*2]
				v3 = viewCounts[splitAt*2:]
				u1 = usefulnessCounts[:splitAt]
				u2 = usefulnessCounts[splitAt:splitAt*2]
				u3 = usefulnessCounts[splitAt*2:]
				
				for row in results:
					id = row[u'Id']
					sqlVup = "SELECT count(Id) as count from Votes where VoteTypeId = 2 and PostId = %s"
					sqlVdown = "SELECT count(Id) as count from Votes where VoteTypeId = 3 and PostId = %s"
					upCount = cursor.execute(sqlVup, (id))
					up = cursor.fetchone()
					downCount = cursor.execute(sqlVdown, (id))
					down = cursor.fetchone()
					row[u'CreationDate'] = str(row[u'CreationDate'])
					row[u'UpVotes'] = up[u'count']
					row[u'DownVotes'] = down[u'count']	
					row[u'ViewCountRank'] = getRange(v1, v2, v3, row[u'ViewCount'])
					row[u'UsefulnessRank'] = getRange(u1, u2, u3, row[u'Usefulness'])
				data = results
			return data		
	except Exception, e:
		print traceback.print_exc()
		return -1
		
def createUserInterest(data):
	try:
		with connection.cursor() as cursor:
			for row in data:
				sql = "SELECT UserId, TopicId FROM UserInterests where UserId = %s and TopicId = %s"
				rowCount = cursor.execute(sql, (row[u'UserId'], row[u'TopicId']))
				if rowCount > 0:
					sql = "UPDATE UserInterests set Weight = %s where UserId = %s and TopicId = %s"
					cursor.execute(sql, (row[u'Weight'], row[u'UserId'], row[u'TopicId']))
					connection.commit()
				else:
					sql = "INSERT INTO UserInterests (UserId, TopicId, Weight) VALUES (%s, %s, %s)"
					cursor.execute(sql, (row[u'UserId'], row[u'TopicId'], row[u'Weight']))
					connection.commit()
		return 1
	except Exception, e:
		print traceback.print_exc()
		return -1
		
def getInterestOfUser(userId):
	try:
		result = []
		with connection.cursor() as cursor:			
			sql = "SELECT UI.UserId, T.Id, T.Name, UI.Weight From UserInterests as UI right join Topics as T on T.id = UI.TopicId \
					where UserId = %s"
			rowCount = cursor.execute(sql, (userId))
			if rowCount > 0:		
				result = cursor.fetchall()						
			else:
				sql = "SELECT T.Id, T.Name from Topics as T"
				
				rowCount = cursor.execute(sql)				
				result = cursor.fetchall()
				for row in result:
					row['UserId'] = userId
					row['Weight'] = 0		
		return result
	except Exception, e:
		print traceback.print_exc()
		return -1
		

