import pymysql.cursors
import datetime
import json
import traceback
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('db.cfg')

connection = pymysql.connect(host=config.get('database','host'),
							 user=config.get('database','username'),
							 password=config.get('database','password'),
							 db = config.get('database','db'),
							 charset = 'utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)


#Method to insert/update start/end time
def updateTimeSpent(data):
	postTypeId = 1
	userId = data["UserId"]
	eventId = 2
	userDisplayName = data["UserName"]
	currentTime = datetime.datetime.now()
	postId = data["PostId"]
	count = -1
	existingstarttime = ""
	existingrowId = -1
	try:
		#Check whether there is a row already present with endtime = null
		with connection.cursor() as cursor:
			sql = """SELECT COUNT(*) FROM `UserEventStore` WHERE `UserId` = %s 
			AND `EventId` = %s AND `EndTime` IS NULL""";
			cursor.execute(sql,(userId,eventId))
			count = cursor.fetchone()
			count = count["COUNT(*)"]
			#print count

		if(count != 0):
			with connection.cursor() as cursor:
				sql = """SELECT `Id`,`StartTime` FROM `UserEventStore` WHERE `UserId` = %s
				AND `EventId` = %s AND `EndTime` IS NULL""";
				cursor.execute(sql,(userId,eventId))
				res = cursor.fetchone()
				#print res
				existingstarttime = res["StartTime"]
				existingrowId = res["Id"]



			timeDiff = currentTime - existingstarttime
			mins = divmod(timeDiff.days * 86400 + timeDiff.seconds, 60)
			#print "mins"
			#print mins
			#print timeDiff
			if(mins[0] <= 30):
				#Time difference between last entry is less than 30 mins, so update the endtime for the previous entry
				#print "if"
				#duration = timeDiff[0]*60 + timeDiff[1]
				duration = mins[0]*60 + mins[1]
				#print duration
				with connection.cursor() as cursor:
					sql = """UPDATE `UserEventStore` SET `EndTime` = %s, `Duration` = %s
					WHERE `Id` = %s"""
					cursor.execute(sql, (currentTime,duration,existingrowId))
		#Insert new row with the sent postId
		with connection.cursor() as cursor:
			sql = """INSERT INTO `UserEventStore` (`UserDisplayName`,
				`UserId`,
				`EventId`,
				`StartTime`,
				`PostId`,
				`PostTypeId`) VALUES (%s, %s, %s, %s, %s, %s)"""
			cursor.execute(sql, (userDisplayName, userId, eventId, currentTime, postId, postTypeId))
		connection.commit()
		return 1
	except Exception, e:
		print traceback.print_exc()
		return -1


#Method for capturing the select action performed by user in a page
def updateSelectAction(data):
	postTypeId = data["PostTypeId"]
	userId = data["UserId"]
	eventId = 3
	userDisplayName = data["UserName"]
	currentTime = datetime.datetime.now()
	postId = data["PostId"]
	try:
		#Insert a new row in the table for text selection action
		with connection.cursor() as cursor:
			sql = """INSERT INTO `UserEventStore` (`UserDisplayName`,
				`UserId`,
				`EventId`,
				`StartTime`,
				`PostId`,
				`PostTypeId`) VALUES (%s, %s, %s, %s, %s, %s)"""
			cursor.execute(sql, (userDisplayName,userId, eventId, currentTime, postId, postTypeId))
		connection.commit()
		return 1
	except Exception, e:
		print traceback.print_exc()
		return -1
