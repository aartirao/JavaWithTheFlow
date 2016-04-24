import pymysql.cursors
import datetime
import traceback
import json
from elasticsearch import Elasticsearch
es = Elasticsearch()

connection = pymysql.connect(host='localhost',
							 user='root',
							 password='aweb',
							 db = 'ANS',
							 charset = 'utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

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
				# The ID of each index is the ID of the post in the Posts table
				docId = row.pop('Id')
				es.index(index="post_search_index", doc_type="post_content", 
						id = docId, body=row)

	except Exception, e:
		print traceback.print_exc()

def searchQuery(query):
	postIds = []
	questionIds = []
	# Return "size" hits for the given query. Size arbitrarily set to 50 
	matches = es.search(index = "post_search_index", q = query, size = 50)
	hits = matches['hits']['hits']
	for hit in hits:
		postIds.append(hit['_id'])

	try:
		with connection.cursor() as cursor:
			# If the ID belongs to a question, add to the result as is. If it 
			# belongs to an answer, find its question ID and add to the result.
			for postId in postIds: 
				sqlPostId = "select `PostTypeId` from `Posts` where `Id` = %s"
				rowCount = cursor.execute(sqlPostId, postId)
				if rowCount > 0:
					postTypes = cursor.fetchall()
					for row in postTypes:
						if row['PostTypeId'] == 1:
							questionIds.append(str(postId))
						elif row['PostTypeId'] == 2:
							sqlParent = "select `ParentId` from `Posts` \
										where `Id` = %s"
							parentRowCount = cursor.execute(sqlParent, postId)
							if parentRowCount > 0:
								parents = cursor.fetchall()
								for record in parents:
									# The parent ID of this answer could already be in
									# the list of hits, if the question itself was 
									# a hit for this query. So skip if present in list.
									if str(record['ParentId']) not in questionIds:
										questionIds.append(str(record['ParentId']))

		return questionIds
	except:
		print traceback.print_exc()
		return -1

if __name__ == "__main__":
	# Run this file initially to create index for Posts table.
	indexPosts()
	# Sample query
	qIdList = searchQuery("abstract class create object")



