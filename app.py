from flask import Flask, render_template, request, redirect, url_for, jsonify, flash 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route("/")
def index():
    return render_template("login_selection.html")

@app.route("/login/<method>", methods=["GET", "POST"])
def login_method(method):
    if request.method == "POST":
        return redirect(url_for("signed_in", username=request.form["j_username"]))
    
    return render_template("login.html", method=method)

@app.route("/signed_in/<username>")
def signed_in(username):
    return render_template("signed_in.html", username=username)

@app.route("/login-selection")
def login_selection():
    return render_template("login_selection.html")

'''
@app.route("/login/<method>", methods=["GET", "POST"])
def login_page(method):
    if request.method == "POST":
        username = request.form.get("j_username")

        return redirect(url_for("signed_in", username=username))

    return render_template("login.html", method=method)

@app.route("/signed-in")
def signed_in_page():
    username = request.args.get("username", "Guest")
    return render_template("signed_in.html", username=username)

'''


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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
