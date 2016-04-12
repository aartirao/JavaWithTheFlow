import pymysql.cursors
import datetime
import traceback
import json


connection = pymysql.connect(host='localhost',
							 user='root',
							 password='1234',
							 db = 'ANS',
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
			sql = """INSERT INTO `posts` (`Id`,
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
				`ClosedDate`) VALUES (%s, %s, %s, %s, %s, %s,
				%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
				%s, %s, %s)"""
				
			cursor.execute(sql, (1, postTypeId, None, parentId, creationDate, None, 
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
			sql = """INSERT INTO `Comments` (`Id`,
				`PostId`,
				`Score`,
				`Text`,
				`CreationDate`,
				`UserDisplayName`,
				`UserId`) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
			cursor.execute(sql, (1,postId, score, text, creationDate, 
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
			sql = """INSERT INTO `posts` (`Id`,
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
				`ClosedDate`) VALUES (%s, %s, %s, %s, %s, %s,
				%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
				%s, %s, %s)"""
				
			cursor.execute(sql, (1, postTypeId, acceptedAnswerId, 
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
	try:
		with connection.cursor() as cursor:
			sql = "SELECT * FROM 'Comments' WHERE 'PostId' = %s"
			cursor.execute(sql, (parentId))
			results = cursor.fetchall()
			for row  in results:
				commentId = row[0]
				commentedUser = row[5]
        		commentedTime = row[4]
        		commentText = row[3]
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
	finally:
		connection.close()

#Method to retrieve answers along with comments
def getAnswers(aId):
	answers = []
	comments = []
	temp = {}
	try:
		#Select the answer with the particular id
		with connection.cursor() as cursor:
			sql = "SELECT * FROM 'Posts' WHERE 'Id' = %s"
			cursor.execute(sql, (aId))
			results = cursor.fetchall()
			for row in results:
				postId = row[0]
				postTypeId = row[1]
				postText =  row[8]
 				answeredByUserName = row[10]
 				answeredUserProfile = "#"
 				answeredDate = row[4]
 				isAcceptedAnswer = "#"
 				usefulness = "#"
 				score = row[6]
 				upvotes = "#"
 				downvotes = "#"

 				answer = {
		            "postId": postId,
		            "postTypeId": postTypeId,
		            "postText": postText,
		            "answeredbyUserName": answeredbyUserName,
		            "answeredbyUserId": answeredbyUserId,
		            "answeredUserProfile": answeredUserProfile,
		            "answeredDate": answeredDate,
		            "isAcceptedAnswer": isAcceptedAnswer,
		            "usefulness": usefulness,
		            "score": score,
		            "upvotes": "#",
		            "downvotes": "#"
        		}

        		comments = getComments(aId)
        		temp = {"answer" : answer, "comments" : comments}
        		answers.append(temp)

		return answers
	except Exception, e:
		print traceback.print_exc()
		return -1
	finally:
		connection.close()



#Method to retrieve post details 
def getQuestion(data):
	qId = data["PostId"]
	question = {}

	try:
		#Select the question with the particular postId
		with connection.cursor() as cursor:
			sql = "SELECT * FROM 'Posts' WHERE 'Id' = %s"
			cursor.execute(sql, (qId))
			results = cursor.fetchall()
			for row in results:
				postId = row[0]
				postTypeId = row[1]
				postTitle = row[15]
				postText = row[8]
				usefulness = "#"
				traffic = "#"
				upvotes = "#"
				downvotes = "#"
				score = row[6]
				isFavorite = "#"
				tags = row[16]
				askedDate = row[4]
				status = "#"
				askedByUserName = row[10]
				askedByUserId = row[9]
				askedUserProfile = "#"
				noOfAnswers = row[17]

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
		answers = getAnswer(qId)
		final = json.dump({"question" : question, "comments" : comments, "answers" : answers})


		connection.commit()
		return final
	except Exception, e:
		print traceback.print_exc()
		return -1
	finally:
		connection.close()

	