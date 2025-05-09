from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from config.config_db import Config
from werkzeug.security import generate_password_hash, check_password_hash

import os
import re

from scripts.graph_data import graph_data  
from scripts.get_class_info import get_class_info
from scripts.query_predictions import query_predictions
from scripts.random_forest import random_forest   
from config.config_db import get_db 
from scripts.run_regression import linear_regression_run

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = os.urandom(24)

AUTH_DIR  = os.path.join(os.path.dirname(__file__), 'authentication')
CRED_FILE = os.path.join(AUTH_DIR, 'credentials.txt')

os.makedirs(AUTH_DIR, exist_ok=True)
if not os.path.exists(CRED_FILE):
    open(CRED_FILE, 'w').close()


""" Related to the login functionality """

class LoginForm(FlaskForm):
    identifier = StringField('Email or NUID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nuid = StringField('NUID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        email = form.email.data
        nuid = form.nuid.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))
        
        hashed = generate_password_hash(password)
        with open(CRED_FILE, 'a') as f:
            f.write(f"{first_name}:{email}:{nuid}:{hashed}\n")
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login_selection'))                 
    return render_template('register.html', form=form)

@app.route("/")
def index():
    return render_template("login_selection.html")

@app.route("/login/<method>", methods=["GET", "POST"])
def login_method(method):
    form = LoginForm()
    if form.validate_on_submit():
        ident = form.identifier.data
        password = form.password.data
        first_name = check_credentials(ident, password)
        if first_name: 
            session['username'] = first_name
            return redirect(url_for('home'))
            # return redirect(url_for('home', username=first_name))
        
        flash("Invalid credentials. Please register first.")
        return redirect(url_for('login_method', method=method))

    return render_template("login.html", method=method, form=form)

@app.route("/home")
# This route shows the successful login and home page 
def home():
    
    username = session.get('username')
    print(username)
    if not username:
        return redirect(url_for('login_method', method='default'))
    
    return render_template("home.html", username=username)

@app.route("/login-selection")
# This route renders the page with 3 login options 
def login_selection():
    return render_template("login_selection.html")

@app.route('/handle_register', methods=['POST'])
def handle_register():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password == confirm_password:
        hashed_password = generate_password_hash(password)
        with open('authentication/credentials.txt', 'a') as f:
            f.write(f'{username}:{hashed_password}\n')
        flash('Registration successful! Please login.')
        return redirect(url_for('login_selection')) 
    else:
        flash('Passwords do not match')
        return 'Passwords do not match', 400

def check_credentials(identifier, password):
    try:
        with open(CRED_FILE, 'r') as f:
            for line in f:
                first_name, email, nuid, pw_hash = line.strip().split(':', 3)
                if (identifier == email or identifier == nuid) and check_password_hash(pw_hash, password):
                    return first_name
    except FileNotFoundError:
        return False

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login_method', method='default'))
""" End of Related to the login functionality """

def normalize_class_code(raw_code):
    """
    This method handles different variations of user input and change it to the valid form 
    param: raw_code: user input 
    returns: the class code in form DEPT xxxx
    """
    match = re.match(r"([A-Za-z]+)\s*([0-9]+)", raw_code)
    if match:
        return f"{match.group(1).upper()} {match.group(2)}"
    return raw_code.upper()

@app.route("/plot",  methods=['GET','POST'])
def plot_data():
    """
    This method display all user input and display what we know about the class 
    param: none 
    return: none - info is rendered to the template 
    """
    db = next(get_db())
   
    sem = request.form.get('semester')
    class_code_raw = request.form.get('class_code').strip()
    class_code = normalize_class_code(class_code_raw)

    # Call import_data to generate the plot for the given class_code and semester
    filename, message = graph_data(class_code, sem)
    if filename and message: 

        # Call get_class_info for some overview info 
        class_name, fall, fyears, spring, syears, discontinued = get_class_info(class_code)

        all_years = sorted(set(fyears + syears))

        fall_data = {y: v for y, v in zip(fyears, fall)}
        spring_data = {y: v for y, v in zip(syears, spring)}

        aligned_fall = [fall_data.get(y, "—") for y in all_years]
        aligned_spring = [spring_data.get(y, "—") for y in all_years]

        # Query the predictions 
        predicted_lr, predicted_rr = query_predictions(class_code, sem)

        username = request.form.get('username', 'Guest')
        return render_template('result_page.html', filename=filename, class_code=class_code, class_name=class_name[0], fall=aligned_fall, years = all_years, spring=aligned_spring, discontinued=discontinued, lr_prediction=predicted_lr, rr_prediction=predicted_rr, username=username)
    
    elif (filename == None and message == None):
        
        # Call get_class_info for some overview info 
        class_name, fall, fyears, spring, syears, discontinued = get_class_info(class_code)

        all_years = sorted(set(fyears + syears))

        fall_data = {y: v for y, v in zip(fyears, fall)}
        spring_data = {y: v for y, v in zip(syears, spring)}

        aligned_fall = [fall_data.get(y, "—") for y in all_years]
        aligned_spring = [spring_data.get(y, "—") for y in all_years]

        # Query the predictions 
        predicted_lr, predicted_rr = query_predictions(class_code, sem)

        username = request.form.get('username', 'Guest')
        return render_template('result_page.html', filename=filename, class_code=class_code, class_name=class_name[0], fall=aligned_fall, years = all_years, spring=aligned_spring, discontinued=discontinued, lr_prediction=predicted_lr, rr_prediction=predicted_rr, username=username)
    
    else: 
        return render_template("home.html", username=session['username'], error=message)
    
@app.route('/linear_regression/<semester>', methods=['GET', 'POST'])
def trigger_regression(semester):
    """
    Endpoint that triggers the linear regression model and returns the results.
    """
    db = next(get_db())
    predictions = linear_regression_run(db, semester)  
    return jsonify(predictions)  # Return the predictions as a JSON response

@app.route('/random_forest/<semester>', methods=['GET', 'POST'])
def rr_regression(semester):
    """
    Endpoint that triggers the random forest model and returns the results.
    """
    db = next(get_db())
    predictions = random_forest(db, semester)  
    return jsonify(predictions)  # Return the predictions as a JSON response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
