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
            sql = """SELECT DISTINCT P.TopicId, T.Name,U.UserId, SUM(IFNULL(Duration,0)) FROM PostTopicMap P JOIN UserEventStore U ON P.PostId = U.PostId 
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
                         "Duration" : str(item["SUM(IFNULL(Duration,0))"])
                         }
            returnData.append(topicData)
            
            #sum = sum + percentageSpent
        
        return returnData
    except Exception, e:
        print traceback.print_exc()
        return -1  
        

def getDataForStack(userId):
    topicCountData = {}
    #countData = {}
    questionCount = []
    ansCount = []
    ansComment = []
    quesComment = []
    
    try:
        with connection.cursor() as cursor:
            sql = """SELECT M.TopicId, Count(*) AS Count FROM Posts P JOIN PostTopicMap M ON P.Id = M.PostId
                     WHERE P.OwnerUserID = %s AND P.PostTypeId = 1 GROUP BY M.TopicId"""
            cursor.execute(sql, (userId))
            questionCount = cursor.fetchall()
            
        
        with connection.cursor() as cursor:
            sql = """SELECT M.TopicId, Count(*) AS Count FROM Posts P JOIN PostTopicMap M ON P.ParentId = M.PostId 
                     WHERE P.OwnerUserID = %s AND P.PostTypeId = 2 GROUP BY M.TopicId"""
            cursor.execute(sql, (userId))
            ansCount = cursor.fetchall()
            
        with connection.cursor() as cursor:
            sql = """SELECT M.TopicId, COUNT(*) AS Count FROM Comments C JOIN Posts P ON P.Id = C.PostId 
                     JOIN PostTopicMap M ON P.Id = M.PostId 
                     WHERE C.UserId =  %s  GROUP BY M.TopicId"""
            cursor.execute(sql, (userId))
            quesComment = cursor.fetchall()
            
        with connection.cursor() as cursor:
            sql = """SELECT M.TopicId, COUNT(*) AS Count FROM Comments C JOIN Posts P ON C.PostId = P.Id JOIN 
                     PostTopicMap M ON P.ParentId = M.PostId 
                     WHERE C.UserId = %s AND P.PostTypeId = 2 GROUP BY M.TopicId"""
            cursor.execute(sql, (userId))
            ansComment = cursor.fetchall()
        connection.commit()    
            
        for id in range(1, 17):
            countdata = {}
            qcount = 0
            for que in questionCount:
                if(que["TopicId"] == id):
                    qcount = que["Count"]
                    break
            acount = 0
            for ans in ansCount:
                if(ans["TopicId"] == id):
                    acount = ans["Count"]
                    break
            cacount = 0
            for ca in ansComment:
                if(ca["TopicId"] == id):
                    cacount = ca["Count"]
                    break
            qacount = 0        
            for qa in quesComment:
                if(qa["TopicId"] == id):
                    qacount = qa["Count"]
                    break
            countdata["Questions"] = qcount
            countdata["Answers"] = acount
            countdata["QuestionComments"] = qacount
            countdata["AnswerComments"] = cacount
            
            with connection.cursor() as cursor:
                sql = """SELECT Name FROM Topics WHERE Id = %s"""
            
                cursor.execute(sql, (id))
                top = cursor.fetchone()
            
                topicCountData[top["Name"]] = countdata
            
        return topicCountData
    except Exception, e:
        print traceback.print_exc()
        return -1      

def getDataForStack1(userId):
    topicCountData = []
    #countData = {}
    questionCount = []
    ansCount = []
    ansComment = []
    quesComment = []
    
    resQues = []
    resAns = []
    resQcomm = []
    resAcomm = []
    try:
        with connection.cursor() as cursor:
            sql = """SELECT M.TopicId, Count(*) AS Count FROM Posts P JOIN PostTopicMap M ON P.Id = M.PostId
                     WHERE P.OwnerUserID = %s AND P.PostTypeId = 1 GROUP BY M.TopicId"""
            cursor.execute(sql, (userId))
            questionCount = cursor.fetchall()
            
        
        with connection.cursor() as cursor:
            sql = """SELECT M.TopicId, Count(*) AS Count FROM Posts P JOIN PostTopicMap M ON P.ParentId = M.PostId 
                     WHERE P.OwnerUserID = %s AND P.PostTypeId = 2 GROUP BY M.TopicId"""
            cursor.execute(sql, (userId))
            ansCount = cursor.fetchall()
            
        with connection.cursor() as cursor:
            sql = """SELECT M.TopicId, COUNT(*) AS Count FROM Comments C JOIN Posts P ON P.Id = C.PostId 
                     JOIN PostTopicMap M ON P.Id = M.PostId 
                     WHERE C.UserId =  %s  GROUP BY M.TopicId"""
            cursor.execute(sql, (userId))
            quesComment = cursor.fetchall()
            
        with connection.cursor() as cursor:
            sql = """SELECT M.TopicId, COUNT(*) AS Count FROM Comments C JOIN Posts P ON C.PostId = P.Id JOIN 
                     PostTopicMap M ON P.ParentId = M.PostId 
                     WHERE C.UserId = %s AND P.PostTypeId = 2 GROUP BY M.TopicId"""
            cursor.execute(sql, (userId))
            ansComment = cursor.fetchall()
        connection.commit()    
            
        for id in range(1, 17):
            top = ""
            with connection.cursor() as cursor:
                sql = """SELECT Name FROM Topics WHERE Id = %s"""          
                cursor.execute(sql, (id))
                top = cursor.fetchone()
                top = top["Name"]
            countdata = {"x" : "", "y" : ""}
            qcount = 0
            for que in questionCount:
                if(que["TopicId"] == id):
                    qcount = que["Count"]
                    break
            countdata["x"] = top
            countdata["y"] = qcount
            resQues.append(countdata)
            countdata = {"x" : "", "y" : ""}
            acount = 0
            for ans in ansCount:
                if(ans["TopicId"] == id):
                    acount = ans["Count"]
                    break
            
            countdata["x"] = top
            countdata["y"] = acount
            resAns.append(countdata)
            countdata = {"x" : "", "y" : ""}
            
            cacount = 0
            for ca in ansComment:
                if(ca["TopicId"] == id):
                    cacount = ca["Count"]
                    break
                    
            countdata["x"] = top
            countdata["y"] = cacount
            resAcomm.append(countdata)
            countdata = {"x" : "", "y" : ""}
            
            qacount = 0        
            for qa in quesComment:
                if(qa["TopicId"] == id):
                    qacount = qa["Count"]
                    break
            
            countdata["x"] = top
            countdata["y"] = qacount
            resQcomm.append(countdata)
            #countdata = {"x" : "", "y" : ""}
            
        topicCountData.append(resQues)
        topicCountData.append(resAns)
        topicCountData.append(resQcomm)
        topicCountData.append(resAcomm)               
        return topicCountData
    except Exception, e:
        print traceback.print_exc()
        return -1      


#print(getDataForStack1(2526083))