from bottle import Bottle, run, template, static_file, get, post, request, response, abort
import pymysql.cursors
from posts import saveAnswer, saveComment, addQuestion
'''
POST - 201 - Created, 200 - OK {error message}
GET - 200 - OK, 404 - Not Found
DELETE - 200 - OK, 404 - Not Found
PUT - 200 - OK, 404 - Not Found
'''
app = Bottle()

connection = pymysql.connect(host='localhost',
							 user='root',
							 password='admin123+',
							 db = 'ans',
							 charset = 'utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)


@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/awww')
@app.route('/awww/')
def index():
    return template('index/mock.html')

# Static Routes
@app.route('/static/<path:path>')
def stylesheets(path):
    return static_file(path, root='index/static')

# Route for posts page
@app.route('/awww/posts')
@app.route('/awww/posts/')
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

#Post service to add comments
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

try:
	with connection.cursor() as cursor:
		# Create a new record
		sql = "INSERT INTO `Sample` (`Id`, `Name`) VALUES (%s, %s)"
		cursor.execute(sql, (2, 'Karthik'))

		#connection is not autocommit by default. So you must commit to save
		#your changes.
		connection.commit()

	with connection.cursor() as cursor:
		#Select a record
		sql = "SELECT `Id`, `Name` FROM `Sample` WHERE `Id` = %s"
		cursor.execute(sql, (1))
		result = cursor.fetchone()
		print(result)
finally:
	connection.close()


run(app, host='localhost', port=8080, debug=True)

