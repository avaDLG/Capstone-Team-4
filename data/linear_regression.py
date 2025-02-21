# ava's first attempt at linear regression to predict cs class enrollment
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


# open up file with extracted data
# i honestly dont know why i wont use a realtive path -- LOOK AT LATER
with open('Capstone-Team-4/data/CS_enrollment.json', 'r') as f:
    course_enrollment = json.load(f)

    # predict enrollment for next semester --> spring 2024 current semester
    predictions = {}

    for course, years in course_enrollment.items():
        X = []
        y = []

        for year, semesters in years.items():
            for semester, students in semesters.items():
                sem_val = 0 if semester == "Fall" else 1  # encode Fall=0, Spring=1
                X.append([int(year), sem_val])
                y.append(students)

        if len(X) > 1:  # only apply regression if there's enough data
            model = LinearRegression()
            model.fit(X, y)

            # predict next semester's enrollment
            last_year = max(map(int, years.keys()))
            last_semester = "Fall" if "Spring" in years[str(last_year)] else "Spring"
            
            if last_semester == "Fall":
                next_semester = "Spring"
                next_year = last_year
            else:
                next_semester = "Fall"
                next_year = last_year + 1

            next_X = np.array([[next_year, 0 if next_semester == "Fall" else 1]])
            predicted_enrollment = int(model.predict(next_X)[0])

            predictions[course] = {f"{next_year} {next_semester}": predicted_enrollment}


    # dump it out and see...
    print(json.dumps(predictions, indent=4))