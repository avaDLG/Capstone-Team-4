from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    # Render the base.html template
    return render_template("base.html")

# Add more routes here once we get there
if __name__ == '__main__':
    app.run() 
