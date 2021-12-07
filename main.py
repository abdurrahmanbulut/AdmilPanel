import json
import os
import pyrebase
import requests
from flask import Flask, render_template, request



firebaseConfig = {
    'apiKey': os.environ['FIREBASE_API_KEY'],
    'authDomain': "groceryadmin-5ac5b.firebaseapp.com",
    'projectId': "groceryadmin-5ac5b",
    'storageBucket': "groceryadmin-5ac5b.appspot.com",
    'messagingSenderId': "281965995985",
    'appId': "1:281965995985:web:8e912b06c143a2d94362f0",
    'databaseURL': "https://groceryadmin-5ac5b-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

app = Flask(__name__)


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == "POST":
        pwd = request.form['user_pwd']
        pwd_check = request.form['user_pwd_check']
        if pwd == pwd_check:
            try:
                email = request.form['user_mail']
                password = request.form['user_pwd']
                new_user = auth.create_user_with_email_and_password(email, password)
                auth.send_email_verification(new_user['idToken'])
                return render_template('verify_email.html')

            except :
                existing_account = "This email already used"
                # if requests.exceptions.HTTPError:
                 # existing_account = "Email is wrong or password is weak"
                return render_template('create_account.html', exist_message=existing_account)
        else:
            return render_template('create_account.html', psw_not_match="Passwords did not match!")

    return render_template('create_account.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['user_email']
        password = request.form['user_pwd']
        try:
            auth.sign_in_with_email_and_password(email, password)
            user_info = auth.sign_in_with_email_and_password(email, password)
            account_info = auth.get_account_info(user_info['idToken'])
            if not account_info['user'][0]['emailVerified']:
                verify_message = 'Please verify your email'
                return render_template('index.html', umessage = verify_message)
            else:
                return render_template('home.html')
        except:
            unsuccessful = 'Please check your credential'
            return render_template('index.html', umessage = unsuccessful)

    return render_template('index.html')


if __name__ == "__main__":
    app.run()
