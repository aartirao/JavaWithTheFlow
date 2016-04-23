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

		#Update the answer count in database for the question
		with connection.cursor() as cursor:
			sql = """UPDATE `Posts` SET 
				`AnswerCount` = `AnswerCount` + 1
				WHERE `Id` = %s"""
			cursor.execute(sql, (parentId))
		connection.commit()
		return 1
	except Exception, e:
		print traceback.print_exc()
		return -1
	finally:
		connection.close()

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
	finally:
		connection.close()

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
				tags, answerCount, 0, 0, None))

		connection.commit()
		return 1
	except Exception, e:
		print traceback.print_exc()
		return -1
	finally:
		connection.close()

#Method to retrieve comments
def getComments(parentId):
	comments = []
	comment = {}
	try:
		with connection.cursor() as cursor:
			sql = "SELECT * FROM `Comments` WHERE `PostId` = %s"
			rowCount = cursor.execute(sql, (parentId))
			if rowCount > 0:
				results = cursor.fetchall()
				for row  in results:					
					commentId = row[u'Id']
					commentedUser = row[u'UserDisplayName']
					commentedTime = str(row[u'CreationDate'])
					commentText = row[u'Text']
					userUrl = "#"
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
	

#Method to retrieve answers along with comments
def getAnswers(parentId):
	answers = []
	comments = []
	temp = {}
	try:
		#Select the answer with the particular id
		with connection.cursor() as cursor:
			sql = "SELECT * FROM `Posts` WHERE `ParentId` = %s"
			rowCount = cursor.execute(sql, (parentId))
			if rowCount > 0:
				results = cursor.fetchall()
				for row in results:					
					postId = row[u'Id']				
					postTypeId = row[u'PostTypeId']
					postText =  row[u'Body']
					answeredByUserName = row[u'OwnerDisplayName']
					answeredByUserId = row[u'OwnerUserId']
					answeredUserProfile = "#"
					answeredDate = str(row[u'CreationDate'])
					isAcceptedAnswer = "#"
					usefulness = "#"
					score = row[u'Score']
					upvotes = "#"
					downvotes = "#"

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
						"downvotes": "#"
					}

					comments = getComments(postId)
					temp = {"answer" : answer, "comments" : comments}
					answers.append(temp)
					

		return answers
	except Exception, e:
		print traceback.print_exc()
		return -1
	
#Method to retrieve post details 
def getQuestion(data):
	qId = data
	question = {}
	
	try:
		#Select the question with the particular postId
		with connection.cursor() as cursor:
			sql = "SELECT * FROM `Posts` WHERE `Id` = %s"
			rowCount = cursor.execute(sql, (qId))
			if rowCount > 0:
				results = cursor.fetchall()
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
					askedUserProfile = "#"
					noOfAnswers = row[u'AnswerCount']

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
						"askedUserProfile": "#",
						"noOfAnswers": noOfAnswers
	  				}

		comments = getComments(qId)
		answers = getAnswers(qId)
		final = {"question" : question, "comments" : comments, "answers" : answers}

		connection.commit()
		return final
	except Exception, e:
		print traceback.print_exc()
		return -1
	
#Method to return view counts for each topic
def getViewCount():
	data = {}
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
						data[row[u'Id']] = temp			
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
	
	
def getQuestionListByTopic(topic):
	data = {}
	try:
		# Get all questions by topic
		# order by P.ViewCount desc
		with connection.cursor() as cursor:
			sql = "SELECT P.Id, P.Title, P.ViewCount, P.OwnerUserId, P.OwnerDisplayName, P.FavouriteCount, P.Tags, \
			P.AnswerCount, P.CreationDate from Posts as P where P.PostTypeId = 1 and P.Id in (select PT.PostId from \
			Topics as T join PostTopicMap as PT on T.Name = %s and PT.TopicId = T.Id) LIMIT 10"
			rowCount = cursor.execute(sql, (topic))	
			if rowCount > 0:
				results = cursor.fetchall()
				sumViewCount = 0
				viewCounts = []
				for row in results:
					viewCounts.append(int(row[u'ViewCount']))
				viewCounts.sort()
				splitAt = rowCount / 3
				v1 = viewCounts[:splitAt]
				v2 = viewCounts[splitAt:splitAt*2]
				v3 = viewCounts[splitAt*2:]
				
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
				data = results
			return data		
	except Exception, e:
		print traceback.print_exc()
		return -1