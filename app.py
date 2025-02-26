from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route("/")
def index():
    # Render the base.html template
    return render_template("login_selection.html")

# TODO: write json out to a page 
@app.route("/regression")
def linear_regression_output():
    with open('data/cs_predictions.json', 'r') as f:
        cs_predictions = json.load(f)
        return jsonify(cs_predictions)
    
@app.route("/filter/<class_code>")
def class_filter(class_code):
    letter = class_code[:4]
    number = class_code[4:]

    with open('data/cs_enrollment.json', 'r') as f:
        cs_enrollment = json.load(f)
    with open('data/cs_predictions.json', 'r') as f:
        cs_prediction = json.load(f)

    return json.dumps(cs_enrollment[f"{letter} {number}"]) + "====> Prediction:" + json.dumps(cs_prediction[f"{letter} {number}"])

# TODO: once it's done, remove the debug mode
if __name__ == '__main__':
    app.run(debug=True) 
