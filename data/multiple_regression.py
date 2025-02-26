# ava's second attempt at regression to predict cs class enrollment
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# Load JSON file
with open("data/CS_enrollment.json", "r") as file:
    enrollment_data = json.load(file)


# FAKE ENROLLMENT DATA -> REPLACE LATER
total_college_enrollment = {
    "2021": 15000,
    "2022": 14800,
    "2023": 15200,
    "2024": 1500
}

fail_rate = 0.05 # percentage


# combining the json file and other data sources (fail-rate and total enrollment)
# into pandas data frame
rows = []
for course, semesters in enrollment_data.items():
    for semester, years in semesters.items():
        for year, enrollment in years.items():
            rows.append({
                "Course": course,
                "Semester": semester,
                "Year": int(year),
                "Enrollment": enrollment,
                "Total_College_Enrollment": total_college_enrollment.get(year),
                "Fail_Rate": fail_rate
            })

'''
this is what the dataframe looks like -> just all the data in a grid format
        Course Semester  Year  Enrollment  Total_College_Enrollment  Fail_Rate
0    CIST 1300     Fall  2021         127                     15000       0.05
1    CIST 1300     Fall  2022         123                     14800       0.05
2    CIST 1300     Fall  2023         173                     15200       0.05
'''

# create dataframe
df = pd.DataFrame(rows)
#print(df)

# model cannot take non-numerical data
# so i am trying "dummy encoding" to make them binary variables of true and false 
df_encoded = pd.get_dummies(df, columns=["Course", "Semester"], drop_first=True)
'''
Year  Enrollment  Total_College_Enrollment  Fail_Rate  ...  Course_CSCI 4950  Course_CSCI 4970  Course_CSCI 4990  Semester_Spring
0    2021         127                     15000       0.05  ...             False             False             False            False
3    2024         132                      1500       0.05  ...             False             False             False            False
4    2022          97                     14800       0.05  ...             False             False             False             True
'''
# print(df_encoded)



