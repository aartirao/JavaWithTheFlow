from scipy.stats.stats import pearsonr
import numpy as np
import pymysql.cursors
import datetime
import traceback
import json
import operator
import ConfigParser
from search import searchQuery

config = ConfigParser.ConfigParser()
config.read('db.cfg')

connection = pymysql.connect(host=config.get('database','host'),
							 user=config.get('database','username'),
							 password=config.get('database','password'),
							 db = config.get('database','db'),
							 charset = 'utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

ratingsData = {}

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
						weight = row[u'Weight']
						ratingsData[user][topic] = weight
			return ratingsData[user]

	except Exception, e:
		print traceback.print_exc()
		return -1

def pearson_correlation(user1, user2):
	user1RatingsDict = getRatings(user1)
	#print user1RatingsDict
	user1Ratings = [user1RatingsDict[topic] for topic in user1RatingsDict]
	user2RatingsDict = getRatings(user2)
	user2Ratings = [user2RatingsDict[topic] for topic in user2RatingsDict]
	return pearsonr(user1Ratings, user2Ratings)[0]

def getAllUsers():
	allUsers = []
	print "In allUsers"
	try:
		with connection.cursor() as cursor:
			sql = """select `Id` from `Users` LIMIT 10"""
			rowCount = cursor.execute(sql)
			if rowCount > 0:
				result = cursor.fetchall()
			for row in result:
				allUsers.append(row[u'Id'])
		#print allUsers
		return allUsers

	except Exception, e:
		print traceback.print_exc()
	return -1

def getSimilarUsers(user):
    # returns the top 5 similar users for a given user.
    print "In getSimilarUsers"
    allUsers = getAllUsers()
    scores = [(pearson_correlation(user, otherUser), otherUser) 
    			for otherUser in allUsers if otherUser != user]
 
    # Sort the similar users so that highest scored user will appear at the first
    scores.sort()
    scores.reverse()
    print scores[0:5]
    return scores[0:5]

def getTopicsToRecommend(user):
	topics = []
	interestedTopics = []
	similarUsers = getSimilarUsers(user)
	userIDs = [record[1] for record in similarUsers]
	for userID in userIDs:
		topics.extend(ratingsData[userID].items())

	interestedTopics = sorted(topics, key=operator.itemgetter(1))[::-1]
	return interestedTopics[0:3]

def recommendQuestions(user):
	topics = getTopicsToRecommend(user)
	questions = []
	for topic in topics:
		questions.append(searchQuery(topic[0], 2))
	print questions
	return questions

if __name__ == "__main__":
	print recommendQuestions('821742')