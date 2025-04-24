from flask import Flask, render_template, request, redirect, url_for, jsonify, flash 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from config.config_db import Config
from werkzeug.security import generate_password_hash, check_password_hash
import os
from scripts.graph_data import graph_data  
from scripts.get_class_info import get_class_info  
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
            return redirect(url_for('home', username=first_name))
        flash("Invalid credentials. Please register first.")
        return redirect(url_for('login_method', method=method))

    return render_template("login.html", method=method, form=form)

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
        with open(CRED_FILE, 'r') as f:
            for line in f:
                first_name, email, nuid, pw_hash = line.strip().split(':', 3)
                if (identifier == email or identifier == nuid) \
                   and check_password_hash(pw_hash, password):
                    return first_name
    except FileNotFoundError:
        pass
    return None
    
""" Related to the login functionality """

@app.route("/plot",  methods=['POST'])
def plot_data():
    # Get a database session from the get_db() function
    db = next(get_db())

    class_code = request.form.get('class_code')
    sem = request.form.get('semester')
    
    # Call import_data to generate the plot for the given class_code and semester
    filename = graph_data(class_code, sem)
    print(filename)

    # Call get_class_info for some overview info 
    class_name, fall, spring, discontinued, predicted = get_class_info(class_code)

    return render_template('result_page.html', filename=filename, class_code=class_code, class_name=class_name[0], fall=fall, spring=spring, discontinued=discontinued, predicted=predicted)

@app.route('/regression_db', methods=['GET'])
def trigger_regression():
    """
    Endpoint that triggers the regression process and returns the results.
    """
    db = next(get_db())
    
    predictions = linear_regression_run(db, semester="Fall")  
    
    return jsonify(predictions)  # Return the predictions as a JSON response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
