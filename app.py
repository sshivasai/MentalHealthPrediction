

#import flask dependencies for web GUI
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt
from functools import wraps
import pypyodbc as odbc
#import other functions and classes
from sqlhelpers import *
from forms import *
from flask_mail import Mail, Message
#other dependencies
import time

import pickle        
import numpy as np
import datetime as dt

#initialize the app
app = Flask(__name__)


#configuring db server
def makeconnection():
    #configure mssql
    server = 'DESKTOP-EPDTTFN'
    database = 'mentalhealth'
    connection_string = 'DRIVER={ODBC Driver 17 for SQL Server}; \
    SERVER='+ server +'; \
    DATABASE='+ database +';\
    Trusted_Connection=yes;'
    conn = odbc.connect(connection_string)
    #print(conn.cursor())
    return conn

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yourmail'
app.config['MAIL_PASSWORD'] = 'yourpassword'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


#wrap to define if the user is currently logged in from session
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, please login.", "danger")
            return redirect(url_for('login'))
    return wrap

#log in the user by updating session
def log_in_user(username):
    users = Table("users", "name", "email", "username", "password","age","gender")
    user = users.getone("username", username)

    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')

#Registration page
@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    users = Table("users", "name", "email", "username", "password","age","gender")
    #if form is submitted
    if request.method == 'POST' and form.validate():
        #collect form data
        username = form.username.data
        email = form.email.data
        name = form.name.data
        gender = form.gender.data
        age = int(form.age.data)
        print(gender)
        #make sure user does not already exist
        if isnewuser(username,email):
            #add the user to mssql and log them in
            password = sha256_crypt.encrypt(form.password.data)
            users.insert(name,email,username,password,age,gender)
            details = Table("details","username","family_history", "benefits", "care_options", "anonymity", "leave", "work_interfere","dateandtime","probabilityofYes","Output")
            details.insert(username,None, None, None, None, None,None,dt.datetime.now(),None,None)
            try:
                msg = Message(
                'Registration Successfull - '+ str(name),
                sender ='urmailaddress@gmail.com',
                recipients = [email]
               )
                msg.body = 'Hi'+str(name)+","'Thank you make a step towards better health'
                mail.send(msg)
                flash("Please Check your email","success")
            except:
                pass
            log_in_user(username)

            return redirect(url_for('dashboard'))


        else:
            flash('User already exists with same emailid/username', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html', form=form)

#Login page
@app.route("/login", methods = ['GET', 'POST'])
def login():
    #if form is submitted
    if request.method == 'POST':
        #collect form data
        username = request.form['username']
        candidate = request.form['password']

        #access users table to get the user's actual password
        users = Table("users", "name", "email", "username", "password","age","gender")
        user = users.getone("username", username)
        if user : 
            accPass = user.get('password')

        #if the password cannot be found, the user does not exist
            if accPass is None:
                flash("Username is not found", 'danger')
                return redirect(url_for('login'))
            else:
                #verify that the password entered matches the actual password
                if sha256_crypt.verify(candidate, accPass):
                    #log in the user and redirect to Dashboard page
                    log_in_user(username)
                    flash('You are now logged in.', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    #if the passwords do not match
                    flash("Invalid password", 'danger')
                    return redirect(url_for('login'))
        else:
            flash("Username is not found", 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')





#logout the user. Ends current session
@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash("Logout success", "success")
    return redirect(url_for('index'))

#Dashboard page

@is_logged_in
@app.route("/dashboard", methods = ['GET', 'POST'])
def dashboard():

    details = Table("details","username","family_history", "benefits", "care_options", "anonymity", "leave", "work_interfere","dateandtime","probabilityofYes","Output")
    detailstable = details.getall()
    print(detailstable)



    details = getdetails(session.get('username'))
    profile = getprofile(session.get('username'))
    profile = list(profile)
    #print(profile)
    if details:
        details = details
        status = details[0][-1]
    else:
        details=None
        status = None
    
    if status == "None":
        status = None
    #"name", "email", "username", "password","age","gender"
    return render_template('dashboard.html',profile=profile,details = details,status = status,datatable=detailstable)

#Index page
@app.route("/")
@app.route("/index")
def index():
    if 'logged_in' in session:
        login = True
    else:
        login = False
    return render_template('index.html',login=login)


@is_logged_in
@app.route("/updateprofile", methods = ['GET', 'POST'])
def updateprofile():
    form = UpdateProfileForm(request.form)
    details = getdetails(session.get('username'))[0]
    profile = getprofile(session.get('username'))
    profile = list(profile)
    #print(details)
    #"name", "email", "username", "password","age","gender"

    name = profile[0]
    username = profile[2]
    email = profile[1]
    age = profile[4]
    gender = profile[5]

    
    family_history = details[1]
    benefits = details[2]
    care_options = details[3]
    anonymity = details[4]
    leave = details[5]
    work_interfere = details[6]
    datetime = details[7]
    #print(datetime)
    probability = details[8]
    status = details[9]

    print(status)
    #if form is submitted
    if request.method == 'POST':
        username = session.get('username')
        name = form.name.data
        email = form.email.data
        age = int(form.age.data)

        family_history = int(form.family_history.data)
        print(family_history)
        benefits = int(form.benefits.data)
        care_options = int(form.care_options.data)
        anonymity = int(form.anonymity.data)
        leave = int(form.leave.data)
        work_interfere = int(form.work_interfere.data)
        print(work_interfere)
        datetime = dt.datetime.now()
        password = form.password.data
        confirmpassword = form.confirm.data

        model = pickle.load(open('SavedModels/modelsvm.pickle', 'rb'))

        updatequery(username,"email",email)
        updatequery(username,"name",name)
        updatequery(username,"age",age)

        if password and  confirmpassword:
            if password != confirmpassword:
                flash("Password Doesn't Match","danger")
                return render_template('updateprofile.html',form=form,name=name,
                username = username,
                email= email,
                gender= gender,
                age = age,
                family_history = family_history,
                benefits = benefits,
                care_options = care_options,
                anonymity = anonymity,
                leave = leave,
                work_interfere = work_interfere,
                datetime = datetime,
                status = status)
            else:
                password = sha256_crypt.encrypt(password)
                updatequery(username,"password",password)
            
        if gender == "Male":
            gender = 1
        elif gender == "Female":
            gender = 0
        else:
            gender = 3
        
        temp_age = age/44
        features = [np.array([temp_age,gender,family_history,benefits,care_options,
                                anonymity,leave,work_interfere])]

        print(features)
        probability = model.predict_proba(features)

        predict = model.predict(features)

        probability = probability[0][1]
        
        if predict >= 0.5:
            status = "You Need a Treatment"
            flash("You Need a Treatment","danger")
        else:
            status = "You are okay"
            flash("You are Okay ","success")

        details = Table("details","username","family_history", "benefits", "care_options", "anonymity", "leave", "work_interfere","dateandtime","probabilityofYes","Output")
        details.insert(username,family_history, benefits, care_options, anonymity, leave,work_interfere,dt.datetime.now(),probability,status)
            
    
    return render_template('updateprofile.html',form=form,name=name,
    username = username,
    email= email,
    gender= gender,
    age = age,
    family_history = family_history,
    benefits = benefits,
    care_options = care_options,
    anonymity = anonymity,
    leave = leave,
    work_interfere = work_interfere,
    datetime = datetime,
    status = status,
    probability = probability)


@is_logged_in

@app.route("/predict", methods = ['GET', 'POST'])
def predict():
    print("hello")
    form = PredictForm(request.form)
    if request.method == 'POST':
        name = form.name.data
        age = int(form.age.data)
        gender = form.gender.data
        family_history = int(form.family_history.data)
        print(family_history)
        benefits = int(form.benefits.data)
        care_options = int(form.care_options.data)
        anonymity = int(form.anonymity.data)
        leave = int(form.leave.data)
        work_interfere = int(form.work_interfere.data)
        print(work_interfere)
        datetime = dt.datetime.now()
        if gender == "Male":
            gender = 1
        elif gender == "Female":
            gender = 0
        else:
            gender = 3
        temp_age = age/44
        features = [np.array([temp_age,gender,family_history,benefits,care_options,
                                anonymity,leave,work_interfere])]

        print(features)
        model = pickle.load(open('SavedModels/modelsvm.pickle', 'rb'))
        probability = model.predict_proba(features)

        predict = model.predict(features)

        probability = probability[0][1]
        
        if predict >= 0.5:
            status = "You Need a Treatment"
            flash("You Need a Treatment","danger")
        else:
            status = "You are okay"
            flash("You are Okay ","success")

        
        details = Table("details","username","family_history", "benefits", "care_options", "anonymity", "leave", "work_interfere","dateandtime","probabilityofYes","Output")
        details.insert(name,family_history, benefits, care_options, anonymity, leave,work_interfere,dt.datetime.now(),probability,status)
        
        return render_template('predict.html',current_probability=probability, current_status = status )
    
    return render_template('predict.html')



#Run app
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug = True)




