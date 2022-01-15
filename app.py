import pyrebase
from flask import Flask, render_template, request, session, flash, url_for, redirect, jsonify, make_response

from functools import wraps
from wtforms import Form, StringField, PasswordField
import json


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap

app = Flask(__name__)
app.secret_key = 'gtusoftwaregroceryapp'

class Person:
    def __init__(self, name, email, password, phoneNumber, image, type, key, wallet):
        self.name = name
        self.email = email
        self.password = password
        self.phoneNumber = phoneNumber
        self.image = image
        self.type = type
        self.key = key
        self.wallet = wallet


class LoginForm(Form):
    username = StringField("Mail")
    password = PasswordField("Password")


firebaseConfigWeb = {
    'apiKey': "AIzaSyCTHK16qs1kP5O2I6GdNHV3IrAbZZj7DqA",
    'authDomain': "groceryadmin-5ac5b.firebaseapp.com",
    'databaseURL': "https://groceryadmin-5ac5b-default-rtdb.firebaseio.com",
    'projectId': "groceryadmin-5ac5b",
    'storageBucket': "groceryadmin-5ac5b.appspot.com",
    'messagingSenderId': "281965995985",
    'appId': "1:281965995985:web:8e912b06c143a2d94362f0"
}

# web
firebaseConfig = {
    'apiKey': "AIzaSyAQdY2VV4QOR_7zGT1PpB1jMRLNKXEB19w",
    'authDomain': "high-lacing-330220.firebaseapp.com",
    'databaseURL': "https://high-lacing-330220-default-rtdb.firebaseio.com",
    'projectId': "high-lacing-330220",
    'storageBucket': "high-lacing-330220.appspot.com",
    'messagingSenderId': "41516160651",
    'appId': "1:41516160651:web:d9fd0340582463b28f268e",
    'measurementId': "G-MGZZQ54S74",
    'serviceAccount': "serviceAccountKey.json"
}

firebase = pyrebase.initialize_app(firebaseConfig)
firebaseWeb = pyrebase.initialize_app(firebaseConfigWeb)
db = firebase.database()


authWeb = firebaseWeb.auth()
auth = firebase.auth()
storage = firebase.storage()



user_list = []
product_list = []


def refresh_users(db):
    users_list = []
    users = db.child("users").get()
    for user in users.each():
        userImage = storage.child("profiles/" + user.key()).get_url(user.key())
        users_list.append(Person(user.val()['name'], user.val()['email'], user.val()['password'], user.val()['phoneNumber'], userImage, user.val()['type'], user.key(), user.val()['wallet']))
    return users_list


user_list = refresh_users(db)




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/")
def send_message():
    return "sent"


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/products")
@login_required
def products():
    return render_template("products.html", data=product_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        email = form.username.data
        password = form.password.data
        try:
            authWeb.sign_in_with_email_and_password(email, password)
            session['logged_in'] = True
            flash("Successfully logged in!")
            return redirect(url_for("dashboard"))
        except:
            flash("Invalid email or password")
            return redirect(url_for("login"))

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    flash("Good bye!")
    return redirect(url_for("index"))


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['user_email']
        try:
            authWeb.send_password_reset_email(email)
            flash("Mail sent successfully")
            return redirect(url_for('dashboard'))
        except:
            flash("Who are you?")
            render_template("reset_password.html")
    return render_template("reset_password.html")



@app.route("/customers")
@login_required
def customers():
    user_list = refresh_users(db)
    return render_template("customers.html", data=user_list)



@app.route("/ajax_add",methods=["POST","GET"])
def ajax_add():
    if request.method == 'POST':
        txtname = request.form['txtname']
        txtemail = request.form['txtemail']
        txtpassword = request.form['txtpassword']
        txtphone = request.form['txtphone']
        txttype = request.form['txttype']
        txtkey = ""

        if txttype == "cashier" or txttype == "Cashier": txttype_no = 1
        elif txttype == "Costumer" or txttype == "costumer" or txttype == "Customer" or txttype == "customer": txttype_no = 0 
        else : txttype_no = 0
        
        if txtname == '':
            msg = 'Please Input name'  
        else:        
            data = {'name':txtname, 'email':txtemail, 'password':txtpassword, 'phoneNumber':txtphone, 'image': '', 'type':txttype_no, 'wallet': 0}
            try:
                customer = auth.create_user_with_email_and_password(txtemail, txtpassword)
                data.update({"uid": customer['localId']})
                temp = db.child("users").push(data)
                txtkey = temp['name']
                msg = 'New record created successfully' 
            except:
                msg = "Invalid mail or password"
                
    result = msg + "," + txtkey
    return result

#storage.child("profiles").child("sdfdsadf").put("static/image/cart.png")
@app.route("/ajax_update",methods=["POST","GET"])
def ajax_update():
    msg = ""

    if request.method == 'POST':
        txtname = request.form['txtname']
        txtemail = request.form['txtemail']
        txtpassword = request.form['txtpassword']
        txtphone = request.form['txtphone']
        txttype = request.form['txttype']
        txtkey = request.form['txtkey']

        if txttype == "cashier" or "Cashier": txttype_no = 1
        elif txttype == "Costumer" or "costumer" or "Customer" or "customer": txttype_no = 0 
        else: txttype = 0

        current_user = db.child("users").child(txtkey).get()
        old_email = current_user.val()['email']
        old_password = current_user.val()['password']

        if old_password == txtpassword and old_email == txtemail:
            try:
                db.child("users").child(txtkey).update(
                    {'name': txtname, 'phoneNumber': txtphone, 'type': txttype_no})
                msg = 'Record successfully Updated'
            except:
                print("db is broken")
        else:
            try:

                user = auth.sign_in_with_email_and_password(old_email, old_password)
                auth.delete_user_account(user['idToken'])
                newCustomer = auth.create_user_with_email_and_password(txtemail, txtpassword)
                db.child("users").child(txtkey).update(
                    {'name': txtname, 'email': txtemail, 'password': txtpassword, 'phoneNumber': txtphone,
                      'type': txttype, 'uid': newCustomer['localId']})
            except:
                msg = "Invalid Email/Password"
    
    return msg
 
@app.route("/ajax_delete",methods=["POST","GET"])
def ajax_delete():
    msg = ""
    if request.method == 'POST':

        getid = request.form['userKey']
        email = db.child("users").child(getid).get().val()["email"]
        password = db.child("users").child(getid).get().val()["password"]
        
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            auth.delete_user_account(user['idToken'])
        except:
            print("user deleted just from database")

        db.child("users").child(getid).remove()
        msg = 'Record deleted successfully'
        
    return msg


@app.route("/ajax_get_url",methods=["POST","GET"])
def ajax_get_url():
    
    if request.method == 'POST':

        getUrl = request.form['imageUrl']
        print(getUrl)
        
    return "loaded"


if __name__ == "__main__":
    app.run(debug=True)
