from bottle import Bottle, run, template, static_file, get, post, request, response, abort
import pymysql.cursors


from posts import saveAnswer, saveComment, addQuestion, getQuestion, getViewCount, \
		getSortedQuestionListByTopic, saveUserRating, createBookmark, getQuestionListByBookmark, createUserInterest, \
		getInterestOfUser
from users import checkPassword, createUser, getUserId
from browserEvents import updateTimeSpent, updateSelectAction,updateViewCount
from recommendation import recommendQuestions

from search import searchQuery
from users import follow, unFollow, getUserDetails, getAllDetailsOfUser
from search import searchQuery, fetchResults

from vis import getDataForPie

import ConfigParser

config = ConfigParser.ConfigParser()
config.read('db.cfg')

'''
POST - 201 - Created, 200 - OK {error message}
GET - 200 - OK, 404 - Not Found
DELETE - 200 - OK, 404 - Not Found
PUT - 200 - OK, 404 - Not Found
'''
app = Bottle()

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/mainPage')
def index():
	username = request.GET.get('username')
	return template('index/index.html', username=username)

@app.route('/loginPage')
def index():
    return template('index/login.html')

@app.route('/awww')
@app.route('/awww/')
def index():
    return template('index/mock.html')

# Static Routes
@app.route('/static/<path:path>')
def stylesheets(path):
    return static_file(path, root='index/static')

# Route for posts page
@app.route('/posts')
@app.route('/posts/')
def index(): 
	username = request.GET.get('username')
	return template('index/posts.html', username=username)

@app.route('/login', method='POST')
def login():

    username = request.forms.get('username')
    password = request.forms.get('password')
    
    if (username == 'karthik' and password == 'hello'):
        response.status = 201
        return {"status": "success"}    
    else:
        response.status = 401
        return {"status": "user does not exist"}

#Post service to add answers
@app.route('/saveAnswer', method='POST')
def postAnswer():
	data = request.json
	returnValue = saveAnswer(data)
	if(returnValue != -1):
		response.status = 201
		return {"status": "successfully saved", "postId": returnValue}
	else:
		response.status = 200
		return {"status": "some error occured"}

#Post service to add comments
@app.route('/saveComment', method='POST')
def postComment():
	data = request.json
	returnValue = saveComment(data)
	if(returnValue == 1):
		response.status = 201
		return {"status": "successfully saved"}
	else:
		response.status = 200
		return {"status": "some error occured"}

		response.status = 200
		return {"status": "successfully retrieved", "data": returnValue}

#Post service to add questions
@app.route('/addQuestion', method='POST')
def postQuestion():
	data = request.json
	returnValue = addQuestion(data)
	if(returnValue == 1):
		response.status = 201
		return {"status": "successfully saved"}
	else:
		response.status = 200
		return {"status": "some error occured"}

#Get service to retrieve posts
@app.route('/getQuestion/<qId>', method ='GET')
@app.route('/getQuestion/<qId>/<uId>', method ='GET')
def findQuestion(qId,uId=0):
	returnValue = getQuestion(qId,uId)
	if(returnValue == -1):
		response.status = 404
		return {"status": "not found"}
	else:
		response.status = 200
		return {"status": "successfully retrieved", "data": returnValue}

#Get service to retrieve view counts
@app.route('/getViewCount', method ='GET')
def getViews():
	returnValue = getViewCount()
	if(returnValue == -1):
		response.status = 404
		return {"status": "not found"}
	else:
 		response.status = 200
 		return {"status": "successfully retrieved", "data": returnValue}

#Method to get the list of questions for a topic (First page of results)
@app.route('/getQuestionList/<topic>', method='GET')
def getQuestionList(topic):
	#returnValue = getQuestionListByTopic(topic)
	returnValue = searchQuery(topic, 70)
	if(returnValue == -1):
		response.status = 404
		return {"status": "not found"}
	else:
		response.status = 200
		return {"status": "successfully retrieved", "data": returnValue}

#Method to get the list of questions for a topic (Pages 2 to 5)
@app.route('/getQuestionList/<topic>/<pageId>', method='GET')
def getQuestionListResults(topic, pageId):
	returnValue = fetchResults(pageId)
	if(returnValue == -1):
		response.status = 404
		return {"status": "not found"}
	else:
		response.status = 200
		return {"status": "successfully retrieved", "data": returnValue}

#Method to update the time spend by user in a page
@app.route('/updateTime', method = 'POST')
def updateTime():
	data = request.json
	returnValue = updateTimeSpent(data)
	if(returnValue == 1):
		response.status = 201
		return {"status": "successfully saved"}
	else:
		response.status = 200
		return {"status": "some error occured"}

#Method to update the text selection action performed by the user
@app.route('/updateSelectAction', method = 'POST')
def updateSelect():
	data = request.json
	returnValue = updateSelectAction(data)
	if returnValue == 1:
		response.status = 201
		return {"status": "successfully saved"}
	else:
		response.status = 200
		return {"status": "some error occured"}

#Method to return search results for a given query (Page 1)
@app.route('/search/<query>', method = 'GET')
def callSearch(query):
	returnValue = searchQuery(query, 70)
	if(returnValue == -1):
		response.status = 404
		return {"status": "not found"}
	else:
		response.status = 200
		return {"status": "successfully retrieved", "data": returnValue}
	
#Method to return search results for a given query (Pages 2 to 5)
@app.route('/search/<query>/<pageId>', method = 'GET')	
def callSearchResults(query, pageId):
	returnValue = fetchResults(pageId)
	if(returnValue == -1):
		response.status = 404
		return {"status": "not found"}
	else:
		response.status = 200
		return {"status": "successfully retrieved", "data": returnValue}

#Method to save the user ratings
@app.route('/saveUserRating', method = 'POST')
def saveUserRatingScore():
	data = request.json
	returnValue = saveUserRating(data)
	if(returnValue == 1):
		response.status = 201
		return {"status": "successfully saved"}
	else:
		response.status = 200
		return {"status": "some error occured"}
		
#Method to updating view count
@app.route('/updateViewCount', method = 'POST')
def updateViewCountForQuestions():
	data = request.json
	returnValue = updateViewCount(data)
	if(returnValue == 1):
		response.status = 201
		return {"status": "successfully saved"}
	else:
		response.status = 200
		return {"status": "some error occured"}

@app.route('/questionList', method='GET')
def questionList():
	username = request.GET.get('username')
	return template('index/questions.html',username=username)


""" Sample
{
    "PostId": 27727407,
    "UserId": 2
}
"""

@app.route('/bookmark', method='POST')
def addBookmark():
	data = request.json	
	returnValue = createBookmark(data['UserId'], data['PostId'])
	if returnValue == 1:
		response.status = 201
		return {"status": "successfully saved"}
	else:
		response.status = 200
		return {"status": "some error occured"}

@app.route('/getBookmarks/<userId>', method='GET')
def getQuestionList(userId):
	returnValue = getQuestionListByBookmark(userId)
	if(returnValue == -1):
		response.status = 404
		return {"status": "not found"}
	else:
		response.status = 200
		return {"status": "successfully retrieved", "data": returnValue}

@app.route('/getRecommendations/<userId>', method='GET')
def getQuestionList(userId):
	returnValue = recommendQuestions(userId)
	if(returnValue == -1):
		response.status = 404
		return {"status": "not found"}
	else:
		response.status = 200
		return {"status": "successfully retrieved", "data": returnValue}


""" Sample
[
    { "UserId": 2, "TopicId": 2, "Weight": 4},
    { "UserId": 2, "TopicId": 1, "Weight": 1},
    { "UserId": 2, "TopicId": 3, "Weight": 2},
    { "UserId": 2, "TopicId": 4, "Weight": 3},
    { "UserId": 2, "TopicId": 5, "Weight": 4}
]
"""


@app.route('/userInterest', method='POST')
def addUserInterest():
	data = request.json	
	returnValue = createUserInterest(data)
	if returnValue == 1:
		response.status = 201
		return {"status": "successfully saved"}
	else:
		response.status = 200
		return {"status": "some error occured"}
			
#Route for ask question page
@app.route('/ask', method = 'GET')
def askQuestion():
	return template('index/ask.html')
		
@app.route('/getInterest/<userId>', method='GET')
def getInterest(userId):
	returnValue = getInterestOfUser(userId)
	if(returnValue == -1):
		response.status = 404
		return {"status": "not found"}
	else:
		response.status = 200
		return {"status": "successfully retrieved", "data": returnValue}

@app.route('/interest', method = 'GET')
def interest():
	return template('index/interest.html')
	
@app.route('/follow', method = "POST")
def followUser():
	data = request.json
	returnValue = follow(data)
	if returnValue == 1:
		response.status = 201
		return {"status": "successfully saved"}
	else:
		response.status = 200
		return {"status": "some error occured"}
		
@app.route('/unfollow', method = "POST")
def unFollowUser():
	data = request.json
	returnValue = unFollow(data)
	if returnValue == 1:
		response.status = 201
		return {"status": "successfully saved"}
	else:
		response.status = 200
		return {"status": "some error occured"}


#Method to verify password
@app.route('/checkPassword', method = 'POST')
def verifyPassword():
	data = request.json
	returnValue = checkPassword(data)
	if(returnValue == 1):
		response.status = 200
		return {"status": "successfully saved", "result" : returnValue}
	else:
		response.status = 404
		return {"status": "some error occured", "result" : returnValue}

#Method to add a user
@app.route('/createUser', method = 'POST')
def addUser():
	data = request.json
	returnValue = createUser(data)
	if(returnValue == 1):
		response.status = 201
		return {"status": "successfully saved", "result" : returnValue}
	else:
		response.status = 200
		return {"status": "some error occured", "result" : returnValue}

#Method to get user id
@app.route('/getUserId/<userName>', method = 'GET')
def userId(userName):
	data = request.json
	returnValue = getUserId(userName)
	if(returnValue == -1):
		response.status = 404
		return {"status": "not found"}
	else:
		response.status = 200
		return {"status": "success", "result" : returnValue}

@app.route('/getUserDetails/<uId>', method = "GET")
def userDetails(uId):
	returnValue = getAllDetailsOfUser(uId)
	if(returnValue == -1):
		response.status = 404
		return {"status": "not found"}
	else:
		response.status = 200
		return {"status": "success", "result" : returnValue}

@app.route('/bookmarkList', method='GET')
def bookmarkList():
	username = request.GET.get('username')
	return template('index/bookmarks.html',username=username)

@app.route('/profile', method = 'GET')
def interest():
	return template('index/profile.html')

@app.route('/piechartdata/<userName>', method = "GET")
def getpiechartdata(userName):
	userId = getUserId(userName)
	returnValue = getDataForPie(userId)

@app.route('/searchQuery', method='GET')
def callSearch():
	username = request.GET.get('username')
	return template('index/search.html',username=username)

#Method to get sorted list of questions for a topic 
@app.route('/getSortedQuestionList/<topic>/<parameter>', method='GET')
@app.route('/getSortedQuestionList/<topic>/<parameter>/<page>', method='GET')
def getQuestionList(topic, parameter, page=1):
	print "called"
	returnValue = getSortedQuestionListByTopic(topic,parameter,page)
	if(returnValue == -1):
		response.status = 404
		return {"status": "not found"}
	else:
		response.status = 200
		return {"status": "success", "result" : returnValue}
	
		return {"status": "successfully retrieved", "data": returnValue}
	
run(app, host=config.get('database','host'), port=config.get('database','port'), debug=True)





