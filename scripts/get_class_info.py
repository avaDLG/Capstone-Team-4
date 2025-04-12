import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from config.config_db import engine  # Import database connection

def get_class_info(class_code):
    """
    This function fetches enrollment and headcount data from the database
    for the given class code and semester.
    """

    # Create a session
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # Retrieve the class name 
    class_name = ""
    try:
        class_name_query = text("""
            SELECT Class_Name FROM project_data.enrollment_data
            WHERE Class_Code = :class_code LIMIT 1
        """)
        result = session.execute(class_name_query, {"class_code": class_code}).fetchone()
        class_name = [row for row in result]

    except Exception as e:
        print("Error fetching headcount data:", e)
        session.rollback()
        return
       
    # Retrieve the number of offerings in Fall 
    fall_offerings = []
    try:
        fall_query = text("""
            SELECT Enrollment FROM project_data.enrollment_data
            WHERE Class_Code = :class_code AND Semester = :semester
        """)
        result = session.execute(fall_query, {"class_code": class_code, "semester": "Fall"})
        fall_offerings = [row.Enrollment for row in result]

    except Exception as e:
        print("Error fetching data:", e)
        session.rollback()
        return
    
    # Display the number of offerings in Spring 
    spring_offerings = []
    try:
        spring_query = text("""
            SELECT Enrollment FROM project_data.enrollment_data
            WHERE Class_Code = :class_code AND Semester = :semester
        """)
        result = session.execute(spring_query, {"class_code": class_code, "semester": "Spring"})
        spring_offerings = [row.Enrollment for row in result]

    except Exception as e:
        print("Error fetching data:", e)
        session.rollback()
        return

    discontinued = ""
    try:
        dist_class_query = text("""
            SELECT EXISTS (
                SELECT 1 FROM discontinued_classes WHERE Class_Code = :class_code
            ) AS is_discontinued;
        """)
        result_dist = session.execute(dist_class_query, {"class_code": class_code}).fetchone()
        if result_dist == (1,):
            discontinued = "Has Been Discontinued"
    except Exception as e:
        print("Error fetching data:", e)
        session.rollback()
        return
    
    prediction = []
    try:
        prediction_query = text("""
            SELECT semester, predicted_enrollment FROM project_data.predictions 
            WHERE Class_Code = :class_code AND Semester = :semester
        """)
        result = session.execute(prediction_query, {"class_code": class_code, "semester": "Fall"})
        if result:
            for row in result: 
                prediction.append(f"{row.semester} - {row.predicted_enrollment}")
    except Exception as e:
        print("Error fetching data:", e)
        session.rollback()
        return

    print(prediction)
    return class_name, fall_offerings, spring_offerings, discontinued, prediction
