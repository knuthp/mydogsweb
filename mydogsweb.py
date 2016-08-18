from flask import Flask, request
from os import environ
from flask_stormpath import StormpathManager
from flask_stormpath import user
from flask_login import login_required
from flask_bootstrap import Bootstrap
from flask.templating import render_template
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Link, Subgroup
import imageview
from flask.wrappers import Response
import logging
from dogcamsettings import DogCamSettings
import datetime


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

logging.getLogger().setLevel(logging.INFO)

imageService = imageview.ImageService()
dogCamSettings = DogCamSettings()


@nav.navigation()
def mynavbar():
    return Navbar(
        'MyDogs',
        View('Home', 'root'),
#    View('Templates', 'jinja'),
    View('DogCam', 'dogcam'),
    View('DogCam Settings', 'dogcamsettings'),
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
    dates = imageService.getAvailableDates()
    datesString = [imageService.dateToIsoString(x) for x in dates]
    latest = imageService.getLatest()['path']
    images = [{'name' : 'myImageName2', 'dateTime' : '2016-08-09 13:32:24.1'}]
    return render_template('dogcam.html', images=images, dates=datesString, latest=latest)


@app.route('/dogcam/settings')
@login_required
def dogcamsettings():
    return render_template('dogcamsettings.html')


@app.route('/api/dogcam/settings/',  methods=['POST'])
@login_required
def apidogcamsettings():
    record = (request.form.get('doRecord') == 'on')
    interval = get_sec(request.form.get('interval'))
    dogCamSettings.publishChanges({'doRecord' : record, 'interval' : interval})
    logging.info("Updated settings doRecord={0}, interval={1}".format(record, interval))
    return "OK"

@app.route('/api/dogcam/images/<dayString>', methods=['DELETE'])
@login_required
def apidogcamimagesdelete(dayString):
    day = datetime.datetime.strptime(dayString, "%Y-%m-%d")
    print(day)
    imageService.deleteDay(day)
    return "OK"

@app.route('/latest')
@login_required
def latestImage():
    latest = imageService.getLatest()
    data = imageService.getImage(latest['path'])
    return Response(data, mimetype='image/jpg')

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


if __name__ == '__main__':
    app.run()