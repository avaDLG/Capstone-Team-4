from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Import text from SQLAlchemy

app = Flask(__name__)

# Configure the URI to use the local proxy address
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://fall25team4db:=0Ts4HucO?;5MhVj@127.0.0.1:3306/project_data"

db = SQLAlchemy(app)

@app.route('/test_db')
def test_db():
    try:
        # Use engine.connect() to execute a raw SQL query
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM project_data.FALL_ENRLL"))
            return f"Database connection successful! Result: {result.fetchone()[0]}"
    except Exception as e:
        return f"Database connection failed: {e}"

if __name__ == "__main__":
    app.run(debug=True)