from bottle import Bottle, run, template, static_file, get, post, request, response, abort
app = Bottle()


'''
POST - 201 - Created, 200 - OK {error message}
GET - 200 - OK, 404 - Not Found
DELETE - 200 - OK, 404 - Not Found
PUT - 200 - OK, 404 - Not Found
'''


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

run(app, host='localhost', port=8000, debug=True)
