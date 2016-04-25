from scipy.stats.stats import pearsonr
import numpy as np
import pymysql.cursors
import datetime
import traceback
import json
import operator
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('db.cfg')

connection = pymysql.connect(host=config.get('database','host'),
							 user=config.get('database','username'),
							 password=config.get('database','password'),
							 db = config.get('database','db'),
							 charset = 'utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

ratingsData = {}

def getQuestionListByTopic(topic):
	data = {}
	try:
		# Get all questions by topic
		# order by P.ViewCount desc
		with connection.cursor() as cursor:
			sql = "SELECT P.Id, P.Title, P.ViewCount, P.OwnerUserId, P.OwnerDisplayName, P.FavouriteCount, P.Tags, \
			P.AnswerCount, P.CreationDate from Posts as P where P.PostTypeId = 1 and P.Id in (select PT.PostId from \
			Topics as T join PostTopicMap as PT on T.Name = %s and PT.TopicId = T.Id) LIMIT 2"
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

def getRatings(user):
	try:
		with connection.cursor() as cursor:
			ratingsData[user] = {}
			sql = """select `TopicId`, `Weight` from `UserInterests` 
					where `UserId` = %s"""
			rowCount = cursor.execute(sql, user)
			if rowCount > 0:
				topics = cursor.fetchall()
				for row in topics:
					sqlTopic = """select `Name` from `Topics` where `Id` = %s"""
					rowCountTopic = cursor.execute(sqlTopic, row[u'TopicId'])
					if rowCountTopic > 0:
						result = cursor.fetchall()[0]
						topic = str(result[u'Name'])
						weight = result[u'Weight']
						ratingsData[user][topic] = weight
			return ratingsData[user]

	except Exception, e:
		print traceback.print_exc()
		return -1


def pearson_correlation(user1, user2):
	user1RatingsDict = getRatings[user1]
	user1Ratings = [row[topic] for topic in user1RatingsDict[user1]]
	user2RatingsDict = getRatings[user2]
	user2Ratings = [row[topic] for topic in user1RatingsDict[user2]]
	return pearsonr(user1Ratings, user2Ratings)[0]

def getAllUsers():
	allUsers = []
    try:
    	with connection.cursor() as cursor:
    		sql = """select `Id` from `Users`"""
    		rowCount = cursor.execute(sql)
    		if rowCount > 0:
    			result = cursor.fetchall()
    			for row in result:
    				allUsers.append(row[u'Id'])
    		return allUsers

    except Exception, e:
		print traceback.print_exc()
		return -1

def getSimilarUsers(user):
    # returns the top 5 similar users for a given user.
    allUsers = getAllUsers()
    scores = [(pearson_correlation(user, otherUser), otherUser) 
    			for otherUser in allUsers if otherUser != user]
 
    # Sort the similar users so that highest scored user will appear at the first
    scores.sort()
    scores.reverse()
    return scores[0:5]

def getTopicsToRecommend(user):
	topics = []
	interestedTopics = []
	similarUsers = getSimilarUsers(user)
	userIDs = [record[1] for record in similarUsers]
	for userID in userIDs:
		topics.append(ratingsData[userID].items())

	interestedTopics = sorted(topics, key=operator.itemgetter(1))[::-1]
	return interestedTopics

def recommendQuestions(user):
	topics = getTopicsToRecommend(user)
	questions = {}
	for topic in topics:
		questions.update(getQuestionListByTopic(topic))
	return questions

if __name__ == "__main__":
	#print recommendQuestions('1')