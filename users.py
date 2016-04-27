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
            
            