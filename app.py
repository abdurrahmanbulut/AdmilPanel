import pyrebase
from flask import Flask, render_template, request, session, flash, url_for, redirect, jsonify
from functools import wraps
from wtforms import Form, StringField, PasswordField, SelectField
from flask_wtf import FlaskForm

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap


class Person:
    def __init__(self, name, email, password, phone_number, image, type, uid, key):
        self.name = name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.image = image
        self.type = type
        self.uid = uid
        self.key = key


class Category:
    def __init__(self, name, image):
        self.name = name
        self.image = image


class SubCategory:

    def __init__(self, name, category):
        self.name = name
        self.category = category


class Product:
    def __init__(self, name, stock, desc, id, discount, price, image, subcategory):
        self.name = name
        self.stock = stock
        self.desc = desc
        self.id = id
        self.discount = discount
        self.price = price
        self.image = image
        self.subcategory = subcategory


class LoginForm(Form):
    username = StringField("Mail")
    password = PasswordField("Password")


class AddProduct(Form):
    name = StringField("Product name")
    price = StringField("Product price")
    stock=StringField("Product stock")
    description=StringField("Product description")


firebaseConfig = {
    'apiKey': "AIzaSyCTHK16qs1kP5O2I6GdNHV3IrAbZZj7DqA",
    'authDomain': "groceryadmin-5ac5b.firebaseapp.com",
    'databaseURL': "https://groceryadmin-5ac5b-default-rtdb.firebaseio.com",
    'projectId': "groceryadmin-5ac5b",
    'storageBucket': "groceryadmin-5ac5b.appspot.com",
    'messagingSenderId': "281965995985",
    'appId': "1:281965995985:web:8e912b06c143a2d94362f0"
}

# web
firebaseConfigWeb = {
    'apiKey': "AIzaSyAQdY2VV4QOR_7zGT1PpB1jMRLNKXEB19w",
    'authDomain': "high-lacing-330220.firebaseapp.com",
    'databaseURL': "https://high-lacing-330220-default-rtdb.firebaseio.com",
    'projectId': "high-lacing-330220",
    'storageBucket': "high-lacing-330220.appspot.com",
    'messagingSenderId': "41516160651",
    'appId': "1:41516160651:web:d9fd0340582463b28f268e",
    'measurementId': "G-MGZZQ54S74"
}



firebase = pyrebase.initialize_app(firebaseConfig)
firebaseWeb = pyrebase.initialize_app(firebaseConfigWeb)
db = firebaseWeb.database()

user_list = []
product_list = []
category_list = []
sub_category_list = []
promotion_list = []

class ProductForm(FlaskForm):
    form_cat = SelectField('category', choices=[])
    form_sub = SelectField('subcategory', choices=[])
    form_prod = SelectField('product', choices=[])

print(db.child("users").get())

def refreshUsers(db):
    users_list = []
    users = db.child("users").get()
    for user in users.each():
        users_list.append(Person(user.val()['name'], user.val()['email'], user.val()['password'], user.val()['phoneNumber'], user.val()['image'], user.val()['type'], user.val()['uid'], user.key()))
    return users_list

user_list = refreshUsers(db)

auth = firebase.auth()

app = Flask(__name__)
app.secret_key = 'gtusoftwaregroceryapp'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/")
def send_message():
    return "sent"

@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")



@app.route("/products", methods=['GET', 'POST'])
@login_required
def products():
    categories = db.child("categories").get()
    categoriesJson=[]
    for category in categories.each():
        categoriesJson.append(category.val())

    subCategoriesJson = []
    productListJson = []
    for item in categoriesJson:
        cat = Category(item['name'], item['image'])
        category_list.append(cat)
        subCategoriesJson.append(item["subCategories"])
        for subItem in item["subCategories"]:
            sub_cat = SubCategory(subItem['name'], cat)
            sub_category_list.append((sub_cat))
            for product in subItem["productList"]:
                prod = Product(product["name"], product["count"],product["desc"],
                               product["id"], product["discount"],product["price"],
                               product["image"], sub_cat)
                product_list.append(prod)

    form2 = AddProduct(request.form)
    form = ProductForm()
    form.form_cat.choices=[(category.name) for category in category_list]
    form.form_sub.choices=[(subCategory.name) for subCategory in sub_category_list]
    form.form_prod.choices=[(product.name) for product in product_list]

    if request.method == 'POST':

       if form2.name:
           data={"name":form2.name.data, "price":form2.price.data, "count":form2.stock.data, "id":1, "desc":form2.description.data,"image":"","discount":0}
           for category in categories:
               if category.val()["name"] == form.form_cat.data:
                   for sub in db.child("categories").child(category.key()).child("subCategories").get():
                       if (sub.val()["name"] == form.form_sub.data):
                           db.child("categories").child(category.key()).child("subCategories").child(sub.key()).child(
                               "productList").push(data)

       else:
           for category in categories:
               if category.val()["name"]==form.form_cat.data:
                   for sub in db.child("categories").child(category.key()).child("subCategories").get():
                      if(sub.val()["name"]==form.form_sub.data):
                          for prodItem in db.child("categories").child(category.key()).child("subCategories").child(sub.key()).child("productList").get():
                              if(prodItem.val()["name"]==form.form_prod.data):
                                 db.child("categories").child(category.key()).child("subCategories").child(
                                      sub.key()).child("productList").child(prodItem.key()).remove()




    return render_template("products.html", form=form, product_list=product_list,form2=form2)


@app.route('/subcategory/<get_cat>')
def subcategorybycat(get_cat):
    filteredSubCategories=[]
    for subCategory in sub_category_list:
        if(subCategory.category.name==get_cat):
            print(subCategory.category.name)
            filteredSubCategories.append(subCategory.name)

    return  jsonify({'subcategory' : filteredSubCategories})


@app.route('/product/<sub_cat>')
def productbysubcat(sub_cat):
    filteredProducts=[]
    for prod in product_list:
        if(prod.subcategory.name==sub_cat):
            print(prod.subcategory.name)
            filteredProducts.append(prod.name)

    return  jsonify({'product' : filteredProducts})



@app.route("/admin-promotion")
@login_required
def adminPromotion():
    return render_template("admin-promotion.html")



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        email = form.username.data
        password = form.password.data
        try:
            auth.sign_in_with_email_and_password(email, password)
            session['logged_in'] = True
            flash("You are at home")
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
            auth.send_password_reset_email(email)
            flash("Mail sent successfully")
            return redirect(url_for('dashboard'))
        except:
            flash("Who are you?")
            render_template("reset_password.html")
    return render_template("reset_password.html")



@app.route("/customers")
@login_required
def customers():
    user_list = refreshUsers(db)
    return render_template("customers.html", data=user_list)



@app.route("/ajax_add",methods=["POST","GET"])
def ajax_add():
    if request.method == 'POST':
        txtname = request.form['txtname']
        txtemail = request.form['txtemail']
        txtpassword = request.form['txtpassword']
        txtphone = request.form['txtphone']
        txtimage = request.form['txtimage']
        txttype = request.form['txttype']
        if txttype == "cashier" or "Cashier": txttype_no = 1
        elif txttype == "Costumer" or "costumer" or "Customer" or "customer": txttype_no = 0 
        
        if txtname == '':
            msg = 'Please Input name'  
        else:        
            data = {'name':txtname, 'email':txtemail, 'password':txtpassword, 'phoneNumber':txtphone, 'image':txtimage, 'type':txttype_no, 'uid': db.generate_key()}
            try:
                auth.create_user_with_email_and_password(txtemail, txtpassword)
                db.child("users").push(data)
                msg = 'New record created successfully' 
            except:
                msg = "Invalid mail or password"
        
    return msg


@app.route("/ajax_update",methods=["POST","GET"])
def ajax_update():
    
    if request.method == 'POST':
        txtname = request.form['txtname']
        txtemail = request.form['txtemail']
        txtpassword = request.form['txtpassword']
        txtphone = request.form['txtphone']
        txtimage = request.form['txtimage']
        txttype = request.form['txttype']
        txtuid = request.form['txtuid']
        txtkey = request.form['txtkey']
      
        if txttype == "cashier" or "Cashier": txttype_no = 1
        elif txttype == "Costumer" or "costumer" or "Customer" or "customer": txttype_no = 0

        db.child("users").child(txtkey).update({'name':txtname, 'email':txtemail, 'password':txtpassword, 'phoneNumber':txtphone, 'image':txtimage, 'type':txttype_no, 'uid':txtuid})
        msg = 'Record successfully Updated'   
    return msg  
 
@app.route("/ajax_delete",methods=["POST","GET"])
def ajax_delete():
    
    if request.method == 'POST':
        getid = request.form['string']
        db.child("users").child(getid).remove()
        msg = 'Record deleted successfully'   
    return msg




if __name__ == "__main__":
    app.run(debug=True)
