from flask import Flask, jsonify
import numpy as np
import math
from sklearn.linear_model import LinearRegression
from sqlalchemy import text
from datetime import datetime

# Function to run Linear Regression and predict enrollments
def linear_regression_run(session, semester):
    """
    This function takes in the semester and run a linear regression for enrollment predictions of the class. 
    param: semester Fall/Spring 
    return: a list of each class predictions 
    """
    predictions = []
    
    # Fetch headcount data
    headcount_query = text("SELECT year, enrollment FROM college_headcount WHERE semester = :semester")
    headcount_data = session.execute(headcount_query, {"semester": semester}).fetchall()
    headcount_dict = {year: count for year, count in headcount_data}

    # Fetch course enrollment data
    course_query = text("SELECT class_code, year, enrollment FROM enrollment_data WHERE semester = :semester")
    course_data = session.execute(course_query, {"semester": semester}).fetchall()

    # Loop through each class (using class_code)
    for class_code in set(row[0] for row in course_data):
        X = []  # Current feature: Headcount
        y = []  # Target: Enrollment

        # Filter the course data for the current class_code
        class_data = [row for row in course_data if row[0] == class_code]

        for row in class_data:
            year = row[1]
            enrollment = row[2]

            # Skip years without headcount data
            if year not in headcount_dict:
                continue

            X.append(headcount_dict[year])
            y.append(enrollment)

        # # Ensure there's enough data for the model 
        # if len(X) < 4:
        #     print(f"Not enough data to build the model for {class_code}.")
        #     continue

        # Train the model, excluding 2024 
        model = LinearRegression()
        X = np.array(X[:-1]).reshape(-1, 1)
        model.fit(X, y[:-1])

        # Predict enrollment for the next year
        next_year = max(row[1] for row in class_data)
        if next_year not in headcount_dict:
            print(f"No headcount data available for {next_year}, skipping prediction for {class_code}.")
            continue

        predicted_enrollment = model.predict([[headcount_dict[next_year]]])[0]
        predictions.append((class_code, next_year, math.ceil(predicted_enrollment)))

    # Insert query 
    for class_code, year, predicted_enrollment in predictions:
        session.execute(
            text("""
                INSERT INTO predictions (class_code, year, semester, predicted_enrollment)
                VALUES (:class_code, :year, :semester, :enrollment)
                ON DUPLICATE KEY UPDATE predicted_enrollment = :enrollment
            """),
            {"class_code": class_code, "year": year, "semester": semester, "enrollment": predicted_enrollment},
        )

    session.commit()
    print("Predictions saved successfully.")
    return predictions
