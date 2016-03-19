from bottle import Bottle, run, template, static_file, get
app = Bottle()

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

run(app, host='localhost', port=8080, debug=True)
