from bottle import Bottle, run, template, static_file, get
import pymysql.cursors
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

@app.route('/awww/')
@app.route('/awww/<name>')
def index(name='User'):
    return template('index/mock.html', name=name)

# Static Routes
@app.route('/static/<path:path>')
def stylesheets(path):
    return static_file(path, root='index/static')

# Route for posts page
@app.route('/awww/posts')
@app.route('/awww/posts/')
def index():
    return template('index/posts.html')

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
