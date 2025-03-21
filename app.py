from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login_selection.html")

@app.route("/login/<method>", methods=["GET", "POST"])
def login(method):
    if request.method == "POST":
        return redirect(url_for("signed_in", username=request.form["username"]))
    
    return render_template("login.html", method=method)

@app.route("/signed_in/<username>")
def signed_in(username):
    return render_template("signed_in.html", username=username)

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

@app.route("/login-selection")
def login_selection():
    return render_template("login_selection.html")

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


if __name__ == '__main__':
    app.run(debug=True)
