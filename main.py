#!/usr/bin/env python
from datetime import datetime
from pprint import pprint as pp
from flask import make_response, Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, \
                            login_required, login_user, logout_user 
from data_handler import validateUserLogin, generateSessionEntity, query_data
import uuid
import json
import os
import logging

AUTH_LEVEL = os.environ.get('AUTH_LEVEL')
DEMO_APP_SIGNATURE_CERT_PRIVATE_KEY = os.environ.get('DEMO_APP_SIGNATURE_CERT_PRIVATE_KEY')
MYINFO_CONSENTPLATFORM_SIGNATURE_CERT_PUBLIC_CERT = os.environ.get('MYINFO_CONSENTPLATFORM_SIGNATURE_CERT_PUBLIC_CERT')
MYINFO_APP_CLIENT_ID = os.environ.get('MYINFO_APP_CLIENT_ID')
MYINFO_APP_CLIENT_SECRET = os.environ.get('MYINFO_APP_CLIENT_SECRET')
MYINFO_APP_REALM = os.environ.get('MYINFO_APP_REALM')
MYINFO_APP_REDIRECT_URL = os.environ.get('MYINFO_APP_REDIRECT_URL')

person_test =  {
                    "link" : "http://localhost:3001/myinfo/S9812381D",
                    "users":[
                                {
                                "name":"TAN XIAO HUI",
                                "sex": "F",
                                "race": "CN",
                                "nationality": "SG",
                                "dob":"1970-05-17",
                                "email": "myinfotesting@gmail.com",
                                "mobileno": "+97399245",
                                "regadd": "SG, 128 street BEDOK NORTH AVENUE 4 block 102 postal 460102 floor 09 building PEARL GARDEN", 
                                "hdbtype":"113",
                                "marital": "1",
                                "edulevel": "3",
                                "assessableincome": "1456789.00",
                                "uinfin":"S9812381D"
                                }
                            ]
                }


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)

@app.route('/')
@login_required
def index():
    return redirect(url_for('login'))

@app.route('/dashboard/<userId>')
#@login_required
def dashboard(userId):
    session = generateSessionEntity()
    pp(session)
    link = "http://localhost:3001/myinfo/{}".format(str(session))
    payload = dict()
    payload['link'] = link
    data = query_data(userId)
    payload['users'] = data
    return render_template('dashboard.html', data=payload)

def format_response(res):
    res= json.dumps(res, indent = 4)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

@app.route('/getEnv')
def getEnv():
    res = dict()
    res['authLevel'] = AUTH_LEVEL
    res['privateKey'] = DEMO_APP_SIGNATURE_CERT_PRIVATE_KEY
    res['publickKey'] = MYINFO_CONSENTPLATFORM_SIGNATURE_CERT_PUBLIC_CERT
    res['clientId'] = MYINFO_APP_CLIENT_ID
    res['secretKey'] = MYINFO_APP_CLIENT_SECRET
    res['realm'] = MYINFO_APP_REALM
    res['redirectUrl'] = MYINFO_APP_REDIRECT_URL
    return format_response(res)

@app.route('/myinfo/<sessionId>')
def myInfo(sessionId):
    return render_template('consent_given.html', data=sessionId)

@app.route('/callback')
def callback():
    pp(request)
    return format_response({"result" : "OK"})

@app.route('/test')
def test():
        return render_template(
        'consent_given.html')

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] is not None 
                and request.form['username'] != "" 
                and request.form['password'] is not None 
                and request.form['password'] != "" 
                and validateUserLogin(request.form['username'], request.form['password']) == True):
            user = User(request.form['username'])
            login_user(user)
            return redirect(url_for('dashboard', userId = request.form['username']))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__=='__main__':
    app.run(port=3001, debug=True)