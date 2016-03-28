import pymysql.cursors
import datetime
import traceback


connection = pymysql.connect(host='localhost',
							 user='root',
							 password='admin123+',
							 db = 'ans',
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
