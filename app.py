from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route("/")
def index():
    # Render the base.html template
    return render_template("base.html")

# TODO: write json out to a page 
@app.route("/regression")
def linear_regression_output():

    with open('data/CS_predictions.json', 'r') as f:
        CS_predictions = json.load(f)
     
        return jsonify(CS_predictions)


# TODO: once it's done, remove the debug mode
if __name__ == '__main__':
    app.run(debug=True) 
