from flask import Flask
from os import environ
from flask_stormpath import StormpathManager
from flask_stormpath import user
from flask_login import login_required
from flask_bootstrap import Bootstrap
from flask.templating import render_template
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Link, Subgroup


app = Flask(__name__)

# Configure your app here.
app.config['SECRET_KEY'] = environ['SECRET_KEY']
app.config['STORMPATH_API_KEY_ID'] = environ['STORMPATH_API_KEY_ID']
app.config['STORMPATH_API_KEY_SECRET'] = environ['STORMPATH_API_KEY_SECRET']
app.config['STORMPATH_APPLICATION'] = 'mydogs'
app.config['STORMPATH_ENABLE_REGISTRATION'] = False
app.config['STORMPATH_ENABLE_FORGOT_PASSWORD'] = True

stormpath_manager = StormpathManager(app)
bootstrap = Bootstrap(app) 

nav = Nav()
nav.init_app(app)

@nav.navigation()
def mynavbar():
    return Navbar(
        'MyDogs',
        View('Home', 'root'),
#    View('Templates', 'jinja'),
    View('DogCam', 'dogcam'),
#    View('Admin', 'admins_only'),
    Subgroup(userText(user),
        Link('Login', 'login'),
        Link('Logout', 'logout'))
    )


def userText(user):
    if hasattr(user, 'email'):
        return 'User: ' + user.email
    else:
        return 'Not logged in'



@app.route('/')
def root():
    return render_template('home.html')



@app.route('/dogcam')
@login_required
def dogcam():
    images = [{'name' : 'myImageName2', 'dateTime' : '2016-08-09 13:32:24.1'}]
    return render_template('dogcam.html', images=images)



if __name__ == '__main__':
    app.run()