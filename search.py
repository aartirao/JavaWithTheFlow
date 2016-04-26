import pymysql.cursors
import datetime
import traceback
import json
from elasticsearch import Elasticsearch
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import WordNetLemmatizer
from posts import getRange

es = Elasticsearch()

import ConfigParser

config = ConfigParser.ConfigParser()
config.read('db.cfg')

connection = pymysql.connect(host=config.get('database','host'),
							 user=config.get('database','username'),
							 password=config.get('database','password'),
							 db = config.get('database','db'),
							 charset = 'utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

postIds = []

javaKeywords = """abstract  continue  for  new  switch
assert  default  goto  package  synchronized
boolean  do  if  private  this
break  double  implements  protected  throw
byte  else  import  public  throws
case  enum  instanceof  return  transient
catch  extends  int  short  try
char  final  interface  static  void
class  finally  long  strictfp  volatile
const*  float  native  super  while""".split()

# Method to remove stopwords and lemmatize the words in given text.
def stopWordsAndLemmatize(text):
	wordnet_lemmatizer = WordNetLemmatizer()
	stopWordsSet = set(stopwords.words('english'))
	# Updated punctuations because punctuations could be important for code.
	stopWordsSet.update(set(['.', ',', '"', "'", '?', '!', 
				':', ';', '(', ')', '[', ']', '{', '}']))
	stopWordsSet = stopWordsSet - set(javaKeywords)
	newText = " ".join([wordnet_lemmatizer.lemmatize(word.lower()) 
		for word in text.split() 
		if word.lower() not in stopWordsSet])
	return newText
	
#Method to index Posts table based on Body, Title and Tag fields.
def indexPosts():
	try:
		with connection.cursor() as cursor:
			query = "select Id, PostTypeId, Body, Title, Tags from `Posts`"
			cursor.execute(query)
			c = 1
			for row in cursor:
				print "Row: ", c
				c += 1
				for key in row:
					row[str(key)] = str(row.pop(key))
				# Remove stopwords and lemmatize words in Body and Title
				for key in ('Body', 'Title'):
					row[key] = stopWordsAndLemmatize(row[key])
				# The ID of each index is the ID of the post in the Posts table
				docId = row.pop('Id')
				es.index(index="posts_index", doc_type="posts_table", 
						id = docId, body=row)

	except Exception, e:
		print traceback.print_exc()

def fetchResults(pageId):
	questionIds = []
	data = []
	print pageId
	endIndex = int(pageId) * 10
	startIndex = endIndex - 10
	try:
		with connection.cursor() as cursor:
			# If the ID belongs to a question, add to the result as is. If it 
			# belongs to an answer, find its question ID and add to the result.
			for postId in postIds[startIndex:endIndex]: 
				sqlPostId = "SELECT P.Id, P.Title, P.ViewCount, P.OwnerUserId, P.OwnerDisplayName, P.FavouriteCount, P.Tags, \
			P.AnswerCount, P.CreationDate, P.PostTypeId from Posts as P where P.Id = %s"
				rowCount = cursor.execute(sqlPostId, postId)
				if rowCount > 0:
					postTypes = cursor.fetchall()
					for row in postTypes:
						if row['PostTypeId'] == 1:
							questionIds.append(row)
						elif row['PostTypeId'] == 2:
							sqlParent = "SELECT P.Id, P.Title, P.ViewCount, P.OwnerUserId, P.OwnerDisplayName, P.FavouriteCount, P.Tags, \
			P.AnswerCount, P.CreationDate, P.PostTypeId from Posts as P where P.Id in (SELECT `ParentId` from `Posts` where `Id` = %s) LIMIT 1"
							parentRowCount = cursor.execute(sqlParent, postId)
							if parentRowCount > 0:
								parents = cursor.fetchall()
								for record in parents:
									# The parent ID of this answer could already be in
									# the list of hits, if the question itself was 
									# a hit for this query. So skip if present in list.
									if record not in questionIds:
										questionIds.append(record)
			
			sumViewCount = 0
			viewCounts = []
			for row in questionIds:				
				viewCounts.append(int(row[u'ViewCount']))
			viewCounts.sort()			
			splitAt = len(questionIds) / 3
			v1 = viewCounts[:splitAt]
			v2 = viewCounts[splitAt:splitAt*2]
			v3 = viewCounts[splitAt*2:]
		
			for row in questionIds:
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
			data = questionIds
				
		return data
	except:
		print traceback.print_exc()
		return -1

def searchQuery(query):
	try:
		data = []
		# Remove stopwords from query and lemmatize the words
		query = stopWordsAndLemmatize(query)

		# Return "size" hits for the given query. Size arbitrarily set to 50 
		matches = es.search(index = "posts_index", q = query, size = 70)
		hits = matches['hits']['hits']
		for hit in hits:
			postIds.append(str(hit['_id']))

		data = fetchResults(1)
		return data
	except:
		print traceback.print_exc()
		return -1

if __name__ == "__main__":
	# Run this file initially to create index for Posts table.
	#indexPosts()
	# Sample query
	qIdList = searchQuery("abstract class create object")
	print qIdList



