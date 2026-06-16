import flask
app = flask.Flask(__name__)
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def root(path): return flask.send_from_directory('static', path)
if(__name__ == '__main__'): app.run('0.0.0.0', 8080)
