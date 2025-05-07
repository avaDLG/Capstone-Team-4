import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from config.config_db import engine  # Import database connection

def query_predictions(class_code, semester):
    """
    This function fetches enrollment and headcount data from the database
    for the given class code and semester.
    param: class code, semester 
    return: the predictions from two databases 
    """

    # Create a session
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    # Retrieve the Linear Regression predictions
    lr_prediction = []
    try:
        prediction_query = text("""
            SELECT semester, year, predicted_enrollment, note FROM project_data.predictions 
            WHERE Class_Code = :class_code AND Semester = :semester
        """)
        result = session.execute(prediction_query, {"class_code": class_code, "semester": semester})
        if result:
            for row in result: 
                lr_prediction.append(f"{row.semester} {row.year}")
                lr_prediction.append(f"{row.predicted_enrollment}")
                lr_prediction.append(f"{row.note}")
    except Exception as e:
        print("Error fetching data:", e)
        session.rollback()
        return

    # Retrieve the Random Forest predictions
    rr_prediction = []
    try:
        prediction_query = text("""
            SELECT semester, year, predicted_enrollment, note FROM project_data.rr_predictions  
            WHERE Class_Code = :class_code AND Semester = :semester
        """)
        result = session.execute(prediction_query, {"class_code": class_code, "semester": semester})
        if result:
            for row in result: 
                rr_prediction.append(f"{row.semester} {row.year}")
                rr_prediction.append(f"{row.predicted_enrollment}")
                rr_prediction.append(f"{row.note}")
    except Exception as e:
        print("Error fetching data:", e)
        session.rollback()
        return

    return lr_prediction, rr_prediction
