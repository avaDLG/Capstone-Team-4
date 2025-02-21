from flask import Flask, render_template, jsonify
import json


app = Flask(__name__)

@app.route("/")
def index():
    # Render the base.html template
    return render_template("base.html")

'''
@app.route("/regression")
def linear_regression_output():
    with open('data/CS_predictions.json', 'r') as f:
        CS_predictions = json.load(f)
        return json.dump(CS_predictions, f, indent=4)
'''

# Add more routes here once we get there
if __name__ == '__main__':
    app.run() 
