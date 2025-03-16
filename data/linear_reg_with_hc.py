# ava's first attempt at linear regression to predict cs class enrollment
import json
import numpy as np
import math
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression

def linear_regression_run(input_file_path, sem): 
    """
    This function provides the linear regression based on the previous semesters
    param: the path to the input json file 
    return: none. prediction is written to the cs_predictions_with_hc.json 
    """
    
    predictions = {}
    sem_val = 0 if sem == "Fall" else 1
    # get the head count as X 
    with open('data/cist_head_count.json', 'r') as f:
        head_count = json.load(f)
    
    X = []
    for semester, years in head_count.items():
        if semester == sem: 
            for year, num_students in years.items():
                X.append([int(year), num_students])
    X = np.array(X)

    # open up enrollment file to get the number students as y 
    with open(input_file_path, 'r') as f:
        course_enrollment = json.load(f)
        for course, semesters in course_enrollment.items():
            y = []
            for semester, years in semesters.items():
                if semester == sem: 
                    for year, num_stu in years.items():
                        y.append(num_stu)

                    # only apply regression if there's enough data
                    # NOTE: only consider the ones with all 4 data for now
                    if len(y) >= 4:  
                        model = LinearRegression() 
                        model.fit(X, y)
                        
                        # predict next semester's enrollment
                        last_year = int(X[-1][0])
                        #print(course, semester, year)
                        #print(X)
                        predicted_fall_2024 = model.predict([X[-1]])

                        if course not in predictions: 
                            predictions[course] = {}
                        if semester not in predictions[course]:
                            predictions[course][semester] = {}

                        predictions[course][semester][year] = math.ceil(predicted_fall_2024[0])

    with open("data/cs_predictions_with_hc.json", "w") as f:
        json.dump(predictions, f, indent=4)

def import_data(class_code, sem):
    
    """
    This function reads in the data from cs_enrollment.json for the class code
    """

    with open('data/cist_head_count.json', 'r') as f:
        head_count = json.load(f)
    X_vals = []
    for semester, years in head_count.items():
        if semester == sem: 
            for num_students in years.values():
                X_vals.append(num_students)
    
    y_vals = []
    with open('data/cs_enrollment.json', 'r') as f:
        course_enrollment = json.load(f)

        for semester, years in course_enrollment[class_code].items():
            if semester == sem: 
                for year, num_stu in years.items():
                    y_vals.append(num_stu)

    # Fit a regression line
    m, b = np.polyfit(X_vals, y_vals, 1)  # Linear fit (y = mx + b)

    # Scatter plot
    plt.scatter(X_vals, y_vals, color='blue', label="Actual Data")
    plt.plot(X_vals, [m*x + b for x in X_vals], color='red', label="Best Fit Line")

    # Labels and title
    plt.xlabel("Total College Headcount")
    plt.ylabel(f"{class_code} Enrollments")
    plt.title(f"{class_code} vs College Headcount")
    plt.legend()
    plt.show()

if __name__ == "__main__":

    print("Select an option:")
    print("1 - Run the Model")
    print("2 - Graph a class enrollment")
    user_input = int(input("Option: "))

    if user_input == 1: 
        linear_regression_run('data/cs_enrollment.json', "Fall")
    elif user_input == 2: 
        class_code = input("Enter class code (eg. CSCI 1620): ").strip()
        fall = input("Fall/Spring (case sensitive) ").strip()
        import_data(class_code, fall)