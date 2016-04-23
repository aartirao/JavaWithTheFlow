from bottle import Bottle, run, template, static_file, get, post, request, response, abort
import pymysql.cursors
from posts import saveAnswer, saveComment, addQuestion, getQuestion, getViewCount, getQuestionListByTopic
from browserEvents import updateTimeSpent, updateSelectAction
from search import searchQuery
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
@app.route('/mainPage/')
def index():
    return template('index/index.html')

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
    return template('index/posts.html')

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
	if(returnValue == 1):
		response.status = 201
		return {"status": "successfully saved"}
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
def findQuestion(qId):
	returnValue = getQuestion(qId)
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

@app.route('/getQuestionList/<topic>', method='GET')
def getQuestionList(topic):
	returnValue = getQuestionListByTopic(topic)
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
		return {"status:" "successfully saved"}
	else:
		response.status = 200
		return {"status": "some error occured"}

#Method to update the text selection action performed by the user
@app.route('/updateSelectAction', method = 'POST')
def updateSelect():
	data = request.json
	returnValue = updateSelectAction(data)
	if(returnValue == 1):
		response.status = 201
		return {"status": "successfully saved"}
	else:
		response.status = 200
		return {"status": "some error occured"}

#Method to return search results for a given query
@app.route('/search/<query>', method = 'GET')
def callSearch(query):
	returnValue = searchQuery(query)
	if(returnValue == -1):
		response.status = 404
		return {"status": "not found"}
	else:
		response.status = 200
		return {"status": "successfully retrieved", "data": returnValue}


@app.route('/questionList/', method='GET')
def questionList():
	return template('index/mock2.html')
	
run(app, host='localhost', port=8000, debug=True)

