import os
import sys
import csv
import pymysql.cursors
import traceback

# Connect to the database
# Change username and password before running

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='harinimysql',
                             db='ans',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
postPath = '/Users/hariniravichandran/Documents/Adaptive Web/ANS/Data Dump/Posts/'
commentPath = '/Users/hariniravichandran/Documents/Adaptive Web/ANS/Data Dump/Comments/' 
votePath = '/Users/hariniravichandran/Documents/Adaptive Web/ANS/Data Dump/Votes/' 

topicQueries = {
1: """select Id from Posts 
	where PostTypeId = 1 and
	 MATCH(Body, Title) against ('+inheritance -php -android -C' IN BOOLEAN MODE);""", 

3: """select Id from Posts 
	where PostTypeId = 1 and
	 MATCH(Body) against ('overriding') or 
	MATCH(Body) against ('overloading') or 
	MATCH(Body) against ('polymorphism') or 
	tags like '%polymorphism%';""", 

4: """select Id from Posts 
	where PostTypeId = 1 and
	 MATCH(Body, Title) against ('+*generics* -php -android' IN BOOLEAN MODE);""", 

11: """select Id from Posts 
	where PostTypeId = 1 and
	 MATCH(Body, Title) against ('+"*abstract class*" -php -android' IN BOOLEAN MODE);""",

12: """select Id from Posts 
	where PostTypeId = 1 and
	 Tags like '%string%' or Title like '%string%';""", 

10: """select Id from Posts 
	where PostTypeId = 1 and
	 MATCH(Body, Title) against ('+interface -php -android' IN BOOLEAN MODE);""", 

14: """select Id from Posts where PostTypeId = 1 and
	MATCH(Body, Title) against ('+swing -php -android' IN BOOLEAN MODE) or 
	MATCH(Body, Title) against ('+applet -php -android' IN BOOLEAN MODE);""", 

13: """select Id from Posts 
	where PostTypeId = 1 and
	 MATCH(Body, Title) against ('+servlet -php -android' IN BOOLEAN MODE);""", 

6: """select Id from Posts 
	where tags like '%jvm%';""", 

7: """select Id from Posts  
	where PostTypeId = 1 and
	 MATCH(Body, Title) against ('+*sort* -php -android' in boolean mode);""", 

9: """select Id from Posts 
	where PostTypeId = 1 and
	 MATCH(Body, Title) against ('+constructor -php -android' in boolean mode) 
	or tags like '%constructor%';""", 

5: """select Id from Posts 
	where PostTypeId = 1 and
	 MATCH(Body, Title) against ('+collections -php -android' in boolean mode) 
	or tags like '%collections%';""", 

2: """select Id from Posts where PostTypeId = 1 
	and MATCH(Body, Title) against ('+*thread* -php -android' in boolean mode) 
	or MATCH(Body, Title) against ('+synchronize* -php -android' in boolean mode) 
	or tags like '%thread%' or tags like 'synchronize%';""",

8: """select Id from Posts  
	where PostTypeId = 1 and
	 MATCH(Body, Title) against ('+*factory* -php -android' in boolean mode) 
	or MATCH(Body, Title) against ('+*singleton* -php -android' in boolean mode) 
	or MATCH(Body, Title) against ('+"*design pattern*" -php -android' in boolean mode) 
	or MATCH(Body, Title) against ('+*facade* -php -android' in boolean mode);""",

15: """
	select Id from Posts where PostTypeId = 1 
	and tags like '%class%' or tags like 'object%';
	""",

16: """
	select Id from Posts where PostTypeId = 1 
	and MATCH(Body, Title) against ('+*iterator* -php -android' in boolean mode) 
	or MATCH(Body, Title) against ('+loop* -php -android' in boolean mode) 
	or tags like '%iterator%' or tags like 'loop%';
	"""
}

postsInsertQuery = """INSERT INTO `Posts` 
				(`Id`,
				`PostTypeId`,
				`AcceptedAnswerId`,
				`ParentId`,
				`CreationDate`,
				`DeletionDate`,
				`Score`,
				`ViewCount`,
				`Body`,
				`OwnerUserId`,
				`OwnerDisplayName`,
				`LastEditorUserId`,
				`LastedEditorDisplayName`,
				`LastEditDate`,
				`LastActivityDate`,
				`Title`,
				`Tags`,
				`AnswerCount`,
				`CommentCount`,
				`FavouriteCount`,
				`ClosedDate`) 
				VALUES (%s, %s, %s, %s, %s, %s,
				%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
				%s, %s, %s)"""

commentInsertQuery = """INSERT INTO `Comments` 
				(`Id`,
				`PostId`,
				`Score`,
				`Text`,
				`CreationDate`,
				`UserDisplayName`,
				`UserId`) 
				VALUES (%s, %s, %s, %s, %s, %s, %s)""" 

votesInsertQuery = """INSERT INTO `Votes` 
				(`Id`,
				`PostId`,
				`VoteTypeId`,
				`UserId`,
				`CreationDate`) 
				VALUES (%s, %s, %s, %s, %s)"""

def insertToTable(row, query):
	print "In insertToTable"
	with connection.cursor() as cursor:
		for i in xrange(len(row)):
			# None will be inserted as NULL in the table
			if row[i] == '':
				row[i] = None
			else:
				tempString = ""
			 	for char in row[i]:
			 		if ord(char) > 127:
			 			tempString += ''
			 		else:
			 			tempString += char
			 	row[i] = tempString
		
		try:
			cursor.execute(query, row)
		except:
		 	print traceback.print_exc()
		 	sys.exit()

def processPosts():
	postFiles = []
	for f in os.listdir(postPath):
		if f.endswith(".csv"):
			postFiles.append(f);
	# Just one file for testing 
	# postFiles = ['Answers1.csv']
	for f in postFiles:
		c = 1
		with open(postPath + f, "rb") as csv_file:
			print "Reading"
			reader = csv.reader(csv_file)
			try:
				for row in reader:
					print "Row ", c
					c += 1
					if c == 2:
						continue
					insertToTable(row[:-1], postsInsertQuery)
				connection.commit()
			finally:
				connection.close()

def processComments():
	commentFiles = []
	for f in os.listdir(commentPath):
		if f.startswith("AnswerComments"):
			commentFiles.append(f);
	# Just one file for testing 
	# commentFiles = ['AnswerComments12.csv']
	for f in commentFiles:
		c = 1
		with open(commentPath + f, "rb") as csv_file:
			print "Reading"
			reader = csv.reader(csv_file)
			try:
				for row in reader:
					print "Row ", c
					c += 1
					if c == 2:
						continue
					insertToTable(row, commentInsertQuery)
				connection.commit()
			finally:
				connection.close()

def processVotes():
	voteFiles = []
	for f in os.listdir(votePath):
		if f.startswith("Answer"):
			voteFiles.append(f);
	# Just one file for testing 
	# voteFiles = ['QuestionVotes1.csv']
	try:
		for f in voteFiles:
			c = 1
			with open(votePath + f, "rb") as csv_file:
				print "Reading ", f
				reader = csv.reader(csv_file)
				#try:
				for row in reader:
					print "Row ", c
					c += 1
					if c == 2:
						continue
					insertToTable(row[:-1], votesInsertQuery)
				connection.commit()
	finally:
		connection.close()

def insertTopics():
	print "In insertTopics"
	topics = ['inheritance', 'threads', 'polymorphism', 'generics', 'collections', 
			'jvm', 'sorting', 'design patterns', 'constructors', 'interface', 
			'abstract class', 'string', 'servlet', 'swing', 'classes and objects', 'iterators']

	query = """INSERT INTO `Topics` 
				(`Id`, `Name`) 
				VALUES (%s, %s)
			"""
	count = 1
	with connection.cursor() as cursor:
		try:
			for topic in topics:
				cursor.execute(query, (count, topic))
				count += 1
			connection.commit()
		finally:
			connection.close()

def classifyPostsByTopics():
	print "In classifyPostsByTopics"
	with connection.cursor() as cursor:
		ins_cursor = connection.cursor()
		ins_query = """
						INSERT INTO `PostTopicMap` 
						(`PostId`, `TopicId`) 
						VALUES (%s, %s)
					"""
		try:
			for topic, query in topicQueries.iteritems():
				cursor.execute(query)
				print "Writing topic ", topic
				# print (cursor.description)
				for row in cursor:
					ins_cursor.execute(ins_query, (row['Id'], topic))
				connection.commit()
		finally:
			connection.close()

if __name__ == "__main__":
	processPosts()
	processComments()
	processVotes()
	insertTopics()
	classifyPostsByTopics()

