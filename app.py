from flask import Flask, render_template, request, redirect, url_for, jsonify, flash 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

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
            with open('credentials.txt', 'a') as f:
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
            return redirect(url_for("signed_in", username=username))
        else:
            flash("Invalid credentials. Please register if you don't have an account.")
            return redirect(url_for("login_method", method=method))
    return render_template("login.html", method=method)

@app.route("/signed_in/<username>")
def signed_in(username):
    return render_template("signed_in.html", username=username)

@app.route("/login-selection")
def login_selection():
    return render_template("login_selection.html")

@app.route("/regression")
def linear_regression_output():
    with open('data/cs_predictions.json', 'r') as f:
        cs_predictions = json.load(f)
    
    return jsonify(cs_predictions)

@app.route("/filter-enrollment/<class_code>", methods=["GET"])
def class_filter_enrollment(class_code):
    letter = class_code[:4]
    number = class_code[4:]

    with open('data/cs_enrollment.json', 'r') as f:
        cs_enrollment = json.load(f)
    
    enrollment = cs_enrollment[f"{letter} {number}"]

    return jsonify(enrollment)

@app.route("/filter/<class_code>", methods=["GET"])
def class_filter(class_code):
    letter = class_code[:4]
    number = class_code[4:]

    with open('data/cs_enrollment.json', 'r') as f:
        cs_enrollment = json.load(f)
    with open('data/cs_predictions.json', 'r') as f:
        cs_prediction = json.load(f)
    with open('data/cs_predictions_with_hc.json', 'r') as f:
        cs_prediction_hc = json.load(f)
    
    enrollment = cs_enrollment[f"{letter} {number}"]
    prediction = cs_prediction[f"{letter} {number}"]
    prediction_hc = cs_prediction_hc[f"{letter} {number}"]

    return render_template("data_result.html", 
                           cs_enrollment=enrollment, 
                           cs_prediction=prediction, 
                           cs_prediction_hc=prediction_hc)


@app.route('/handle_register', methods=['POST'])
def handle_register():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password == confirm_password:
        hashed_password = generate_password_hash(password)
        with open('credentials.txt', 'a') as f:
            f.write(f'{username}:{hashed_password}\n')
        flash('Registration successful! Please login.')
        return redirect(url_for('login_selection')) 
    else:
        flash('Passwords do not match')
        return 'Passwords do not match', 400

def check_credentials(username, password):
    try:
        with open('credentials.txt', 'r') as file:
            for line in file:
                stored_username, stored_password_hash = line.strip().split(':', 1)
                if stored_username == username and check_password_hash(stored_password_hash, password):
                    return True
        return False
    except FileNotFoundError:
        return False

if __name__ == '__main__':
    app.run(debug=True, port=5000)
