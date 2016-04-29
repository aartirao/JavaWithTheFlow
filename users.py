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

#Method to follow a user
def follow(data):
	currentUserId = data["UserId"];
	followUserId = data["Follow"];
	count = -1
	try:
		with connection.cursor() as cursor:
			sql = "SELECT COUNT(*) FROM `FollowDetails` WHERE `UserId` = %s AND `FollowingUserId` = %s"
			cursor.execute(sql, (currentUserId, followUserId))
			count = cursor.fetchone()
		if count > 0:
		    #Update the row
			with connection.cursor() as cursor:
				sql = "UPDATE `FollowDetails` SET `isDeleted` = %s WHERE `UserId` = %s AND `FollowingUserId` = %s"
				cursor.execute(sql, (0, currentUserId, followUserId))
		else:
        
			with connection.cursor() as cursor:
				sql = "INSERT INTO `FollowDetails` (`UserId`, `FollowingUserId`, `IsDeleted`) VALUES (%s, %s, %s)"
				cursor.execute(sql, (currentUserId, followUserId, 0))
				connection.commit()
		return 1;
	except Exception, e:
		print traceback.print_exc()
		return -1
			

#Method to verify user - password
def checkPassword(data):

	username = data["username"]
	password = data["password"]
	
	try:
		#Fetch password of user
		with connection.cursor() as cursor:
			sql = "SELECT `Password` from `Users` where `DisplayName` = %s"
			cursor.execute(sql, (username))
			results = cursor.fetchone();
			print password
			print str(results[u'Password'])
			if(str(results[u'Password']) == password):
				print "success"
				return 1

		connection.commit()
		return 0
	except Exception, e:
		print traceback.print_exc()
		return -1

#Method to create a new user
def createUser(data):

	print "Function called - createUser"
	username = data["username"]
	password = data["password"]
	age = data["age"]
	about = data["about"]
	date = "2016-04-20 19:17:00"

	try:
		#Create a new user
		with connection.cursor() as cursor:
			sql = """INSERT INTO `Users` (`Reputation`, `CreationDate`, `DisplayName`, `LastAccessDate`, `Location`, `AboutMe`, `Views`, `UpVotes`, `DownVotes`, `AccountId`, `Age`, `Password`) VALUES(NULL,%s,%s,NULL,NULL,%s,NULL,NULL,NULL,NULL,%s,%s)""";
			cursor.execute(sql, (date, username, about, age, password))
	
		connection.commit()
		return 1
	except Exception, e:
		print traceback.print_exc()
		return -1

#Method to get user id
def getUserId(username):

	try:
		#Get user id
		with connection.cursor() as cursor:
			sql = "SELECT `Id` from `Users` where `DisplayName` = %s"
			cursor.execute(sql, (username))
			result = cursor.fetchone()
			if result[u'Id']:
				return result[u'Id']

		connection.commit()
		return 0 
	except Exception, e:
		print traceback.print_exc()
		return -1
