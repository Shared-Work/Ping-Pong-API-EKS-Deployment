from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
  return 'Server Works!'

@app.route('/health')
def say_hello():
  return 'server is healthy'

@app.route('/hello')
def hello():
  return 'Hello from /hello endpoint'

@app.route('/user/<username>')
def show_user(username):
  return 'Hello %s Happy to see you' % username

