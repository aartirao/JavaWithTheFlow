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
			