from flask import Flask, render_template, request, redirect, url_for, jsonify, flash 
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
from scripts.ridge_regression import ridge_regression   
from config.config_db import get_db 
from scripts.run_regression import linear_regression_run

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = os.urandom(24)

""" Related to the login functionality """

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password == confirm_password:
            hashed_password = generate_password_hash(password)
            with open('authentication/credentials.txt', 'a') as f:
                f.write(f'{username}:{hashed_password}\n')
            flash('Registration successful! Please login.')
            return redirect(url_for('login_selection')) 
        else:
            flash('Passwords do not match')
            return redirect(url_for('register'))  

    return render_template('register.html', form=form)

@app.route("/")
def index():
    return render_template("login_selection.html")

@app.route("/login/<method>", methods=["GET", "POST"])
def login_method(method):
    if request.method == "POST":
        username = request.form.get("j_username")
        password = request.form.get("j_password")
        if check_credentials(username, password):
            return redirect(url_for("home", username=username))
        else:
            flash("Invalid credentials. Please register if you don't have an account.")
            return redirect(url_for("login_method", method=method))
    return render_template("login.html", method=method)

@app.route("/home/<username>")
# This route shows the successful login and home page 
def home(username):
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

def check_credentials(username, password):
    try:
        with open('authentication/credentials.txt', 'r') as file:
            for line in file:
                stored_username, stored_password_hash = line.strip().split(':', 1)
                if stored_username == username and check_password_hash(stored_password_hash, password):
                    return True
        return False
    except FileNotFoundError:
        return False
    
""" End of Related to the login functionality """

def normalize_class_code(raw_code):
    match = re.match(r"([A-Za-z]+)\s*([0-9]+)", raw_code)
    if match:
        return f"{match.group(1).upper()} {match.group(2)}"
    return raw_code.upper()

@app.route("/plot",  methods=['POST'])
# This route generate the plot and all associated data
def plot_data():
    # Get a database session from the get_db() function
    db = next(get_db())
   
    sem = request.form.get('semester')
    class_code_raw = request.form.get('class_code').strip()
    class_code = normalize_class_code(class_code_raw)

    # Call import_data to generate the plot for the given class_code and semester
    filename, message = graph_data(class_code, sem)
    if filename: 
        # Call get_class_info for some overview info 
        class_name, fall, spring, discontinued, predicted = get_class_info(class_code)
        return render_template('result_page.html', filename=filename, class_code=class_code, class_name=class_name[0], fall=fall, spring=spring, discontinued=discontinued, predicted=predicted)
    else: 
        return render_template("home.html", error=message)
    
@app.route('/regression_db', methods=['GET'])
def trigger_regression():
    """
    Endpoint that triggers the regression process and returns the results.
    """
    db = next(get_db())
    predictions = linear_regression_run(db, semester="Fall")  
    return jsonify(predictions)  # Return the predictions as a JSON response

@app.route('/ridge', methods=['GET'])
def ridge_reg():
    """
    Endpoint that triggers the regression process and returns the results.
    """
    db = next(get_db())
    predictions = ridge_regression(db)  
    return jsonify(predictions)  # Return the predictions as a JSON response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
