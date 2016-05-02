import pymysql.cursors
import datetime
import traceback
import json
import ConfigParser

from posts import getRange

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
            count = count["COUNT(*)"]
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
			count = cursor.execute(sql, (username))
			result = cursor.fetchone()
			if count > 0:
				return result[u'Id']            		
		return -1
	except Exception, e:
		print traceback.print_exc()
		return -1
        
#Unfollow method
def unFollow(data):
    currentUserId = data["UserId"]
    followUserId = data["Follow"]
    count = -1
    try:
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM `FollowDetails` WHERE `UserId` = %s AND `FollowingUserId` = %s"
            cursor.execute(sql, (currentUserId, followUserId))
            count = cursor.fetchone()
            count = count["COUNT(*)"]
        if count > 0:
            #unfollow by updating the row
            with connection.cursor() as cursor:
                sql = "UPDATE `FollowDetails` SET `isDeleted` = %s WHERE `UserId` = %s AND `FollowingUserId` = %s"
                cursor.execute(sql, (1, currentUserId, followUserId))
        else:
            return -1;
        connection.commit()
        return 1
    except Exception, e:
        print traceback.print_exc()
        return -1        			
        
        
 #get user details
def getUserDetails(data):
    userId = data
    returnData = {}
    userData = {}
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `Id`, `DisplayName`, `AboutMe`, `CreationDate` FROM `Users` WHERE `Id` = %s"
            rowCount = cursor.execute(sql, (userId))
            if rowCount > 0:
                result = cursor.fetchone()
                DisplayName = result["DisplayName"]
                AboutMe = result["AboutMe"]
                CreationDate = result["CreationDate"]
                UserId = result["Id"]
                returnData = {
                                "UserId" : UserId,
                                "DisplayName" : DisplayName,
                                "AboutMe" : AboutMe,
                                "CreationDate" : str(CreationDate)
                             }
        return returnData
    except Exception, e:
        print traceback.print_exc()
        return -1
        
        
def getAllDetailsOfUser(data):
    userId = data
    returnData = {}
    userData = {}
    followers = []
    following = []
    try:
        userData = getUserDetails(userId)
        print(userId)
        if userData == -1:
            return -1
        with connection.cursor() as cursor:
            sql = "SELECT `FollowingUserId` FROM `FollowDetails` WHERE `UserId` = %s AND `isDeleted` = 0"
            followingCount = cursor.execute(sql, (userId))
            print(followingCount)
            if followingCount > 0:
                res = cursor.fetchall()
                for row in res:
                    followId = row[u'FollowingUserId']
                    temp = getUserDetails(followId)
                    followers.append(temp)
            sql = "SELECT `UserId` FROM `FollowDetails` WHERE `FollowingUserId` = %s AND `isDeleted` = 0"
            followerCount = cursor.execute(sql, (userId))
            print(followerCount)
            if followerCount > 0:
                res = cursor.fetchall()
                for row in res:
                    followerID = row[u'UserId']
                    temp = getUserDetails(followerID)
                    following.append(temp)
        returnData = {
            "UserData" : userData,
            "Followers" : followers,
            "Following" : following
        }
        
        return returnData
    except Exception, e:
        print traceback.print_exc()
        return -1
            
def isActive(userId):
    returnVal = -1
    postcount = 0
    commentcount = 0
  
    try:
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) AS COUNT FROM Posts WHERE OwnerUserId = %s"
            cursor.execute(sql, (userId))
            postcount = cursor.fetchone()
            postcount = postcount["COUNT"]
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) AS COUNT FROM Comments WHERE UserId = %s"
            cursor.execute(sql, (userId))
            commentcount = cursor.fetchone()
            commentcount = commentcount["COUNT"]
        connection.commit()
        
        if postcount >= 10 or commentcount >= 30:
            returnVal = 1
        else:
            returnVal = 0
            
        return returnVal
    except Exception, e:
        print traceback.print_exc()
        return -1    


def getMyQuestions(userId):
    #pageNum = (int(page)-1) * 10;
    data = {}
    try:
        with connection.cursor() as cursor:
            sql = "SELECT P.Id, P.Title, P.ViewCount, P.OwnerUserId, P.OwnerDisplayName, P.FavouriteCount, P.Tags, \
            P.AnswerCount, P.CreationDate, IFNULL(P.Usefulness,0) AS Usefulness from Posts as P where P.PostTypeId = 1 and P.OwnerUserId = %s"
            rowCount = cursor.execute(sql, (userId))
            if rowCount > 0:
                results = cursor.fetchall()
                #print(results)
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
                
def getMyAnswerQuestions(userId):
    #pageNum = (int(page)-1) * 10;
    data = {}
    try:
        with connection.cursor() as cursor:
            sql = "SELECT P.Id, P.Title, P.ViewCount, P.OwnerUserId, P.OwnerDisplayName, P.FavouriteCount, P.Tags, \
            P.AnswerCount, P.CreationDate, IFNULL(P.Usefulness,0) AS Usefulness from Posts as P where P.PostTypeId = 1 \
            AND P.Id IN (SELECT Ps.ParentId FROM Posts as Ps WHERE Ps.PostTypeId = 2 AND Ps.OwnerUserId = %s)"
            rowCount = cursor.execute(sql, (userId))
            if rowCount > 0:
                results = cursor.fetchall()
                #print(results)
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
                


#print(getMyAnswerQuestions(2526083, 1))