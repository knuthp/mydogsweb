from flask import Flask
from os import environ
from flask_stormpath import StormpathManager
from flask_login import login_required
app = Flask(__name__)


# Configure your app here.
app.config['SECRET_KEY'] = environ['SECRET_KEY']
app.config['STORMPATH_API_KEY_ID'] = environ['STORMPATH_API_KEY_ID']
app.config['STORMPATH_API_KEY_SECRET'] = environ['STORMPATH_API_KEY_SECRET']
app.config['STORMPATH_APPLICATION'] = 'mydogs'
app.config['STORMPATH_ENABLE_REGISTRATION'] = False
app.config['STORMPATH_ENABLE_FORGOT_PASSWORD'] = True

stormpath_manager = StormpathManager(app)



@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/secret')
@login_required
def secret():
    return 'Super secret'



if __name__ == '__main__':
    app.run()