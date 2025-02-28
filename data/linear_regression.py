# ava's first attempt at linear regression to predict cs class enrollment
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def linear_regression(input_file_path):
    '''
    This function takes the input file path and runs a linear regression of all semesters'data to provide predictions
    param: enrollment input file 
    return: None (save predictions to the cs_predictions.json file)
    '''
    # open up file with extracted data
    with open(input_file_path, 'r') as f:
        course_enrollment = json.load(f)

        # predict enrollment for next semester --> spring 2024 current semester
        predictions = {}

        for course, semesters in course_enrollment.items():
            X = []
            y = []

            for semester, years in semesters.items():
                for year, students in years.items():
                    sem_val = 0 if semester == "Fall" else 1  # encode Fall=0, Spring=1
                    X.append([sem_val, int(year)])
                    y.append(students)

            if len(X) > 1:  # only apply regression if there's enough data
                model = LinearRegression()
                model.fit(X, y)

                # predict next semester's enrollment
                last_year, last_semester = get_last_year_and_semester(course_enrollment[course])

                # if last_semester == "Spring":
                #     next_semester = "Fall"
                #     next_year = last_year
                # else:
                #     next_semester = "Spring"
                #     next_year = last_year + 1

                next_X = np.array([[0 if last_semester == "Fall" else 1, last_year]])
                predicted_enrollment = int(model.predict(next_X)[0])

                if course not in predictions: 
                    predictions[course] = {}
                if last_semester not in predictions[course]:
                    predictions[course][last_semester] = {}

                predictions[course][last_semester][last_year] = predicted_enrollment

        with open("data/cs_predictions.json", "w") as f:
            json.dump(predictions, f, indent=4)

def get_last_year_and_semester(course_data):
    "This function determines the last year and semester a course's data is available"
    
    # Extract available years for each semester
    fall_years = list(course_data.get("Fall", {}).keys())
    spring_years = list(course_data.get("Spring", {}).keys())

    # Combine and find the most recent year
    all_years = fall_years + spring_years
    last_year = max(map(int, all_years))  # Convert to int to ensure correct ordering

    # Determine last semester
    last_semester = "Fall" if str(last_year) in fall_years else "Spring"

    return last_year, last_semester

if __name__ == '__main__':
    linear_regression('data/cs_enrollment.json')