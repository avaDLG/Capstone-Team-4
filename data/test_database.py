import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    with engine.connect() as connection:
        # when successful, this file should return 'Database connection successful! Result: CIST 1010'
        result = connection.execute(text("SELECT * FROM project_data.FALL_ENRLL LIMIT 1000"))
        print("Database connection successful! Result:", result.fetchone()[0])
except Exception as e:
    print("Database connection failed:", e)