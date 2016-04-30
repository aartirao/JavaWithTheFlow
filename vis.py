import pymysql.cursors
import datetime
import traceback
import json
import ConfigParser
import math

config = ConfigParser.ConfigParser()
config.read('db.cfg')


connection = pymysql.connect(host=config.get('database','host'),
							 user=config.get('database','username'),
							 password=config.get('database','password'),
							 db = config.get('database','db'),
							 charset = 'utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)
                             
def getDataForPie(userId):
    
    timeData = []
    overalltimespent = -1
    returnData = []
    topicData = {}
    try:
        '''
        with connection.cursor() as cursor:
			sql = """SELECT SUM(Res.TimeDuration) FROM ((SELECT DISTINCT P.TopicId, T.Name,U.UserId, U.PostId, SUM(Duration) AS TimeDuration FROM PostTopicMap P 
                     JOIN UserEventStore U ON P.PostId = U.PostId JOIN Topics T ON P.TopicId = T.Id
                     WHERE U.EventId = 2 AND U.UserId = %s GROUP BY P.TopicId, U.UserId, T.Name, U.PostId) AS Res)"""
			cursor.execute(sql, (userId))
			overalltimespent = cursor.fetchone()
        '''
        with connection.cursor() as cursor:
            sql = """SELECT DISTINCT P.TopicId, T.Name,U.UserId, SUM(Duration) FROM PostTopicMap P JOIN UserEventStore U ON P.PostId = U.PostId 
                     JOIN Topics T ON P.TopicId = T.Id 
                     WHERE U.EventId = 2 AND U.UserId = %s GROUP BY P.TopicId, U.UserId, T.Name"""
            cursor.execute(sql, (userId))
            timeData = cursor.fetchall()
        connection.commit()
        #sum = 0
        for item in timeData:
            topicname = item["Name"]
            #percentageSpent = ((item["SUM(Duration)"]/overalltimespent["SUM(Res.TimeDuration)"])*100)
            #topicData[topicname] = str(item["SUM(Duration)"])
            
            topicData = {
                         "Name" : topicname,
                         "Duration" : str(item["SUM(Duration)"])
                         }
            returnData.append(topicData)
            
            #sum = sum + percentageSpent
        
        return returnData
    except Exception, e:
        print traceback.print_exc()
        return -1  
        
