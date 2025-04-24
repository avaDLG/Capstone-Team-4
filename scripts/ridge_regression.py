from flask import Flask, jsonify
import pandas as pd 
import numpy as np
import math
from sqlalchemy import text
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score

def ridge_regression(session):
    """
    This function takes in the semester and run a linear regression for enrollment predictions of the class. 
    param: semester Fall/Spring 
    return: a list of each class predictions 
    """
    
    predictions = []
    
    # # Fetch headcount data
    # headcount_query = text("SELECT year, enrollment FROM college_headcount WHERE semester = :semester")
    # headcount_data = session.execute(headcount_query, {"semester": semester}).fetchall()
    # headcount_dict = {year: count for year, count in headcount_data}

    # Fetch course enrollment data
    erll_query = text("""
        SELECT Class_Code, Class_Name, Year, Semester, Enrollment, Required
        FROM project_data.enrollment_data
        WHERE Enrollment > 0
        ORDER BY year 
    """)
    result = session.execute(erll_query)
    rows = result.fetchall()
    columns = result.keys()  # Gets column names from the query

    df = pd.DataFrame(rows, columns=columns)

    print(df) 

    # Fetch headcount
    hc_query = text("""
            SELECT Enrollment, Year, Semester FROM project_data.college_headcount 
            ORDER BY Year
        """)
    hc_result = session.execute(hc_query)
    hc_rows = hc_result.fetchall()
    hc_columns = hc_result.keys()  # Gets column names from the query

    df_headcount = pd.DataFrame(hc_rows, columns=hc_columns)
    print(df_headcount)

    df_merged = pd.merge(
        df,
        df_headcount,
        on=["Year", "Semester"],  # Join keys
        how="left"
    )

    df_merged["Required"] = df_merged["Required"].astype(int)  # True/False → 1/0
    df_merged = pd.get_dummies(df_merged, columns=["Semester"], drop_first=True)  # One-hot encode semester

    print(df_merged)

    X = df_merged[["Year", "Enrollment_y", "Required", "Semester_Spring", "Class_Code"]]  # features
    y = df_merged["Enrollment_x"]  # target

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"RMSE: {mse**0.5:.2f}")
    print(f"R^2 Score: {r2:.2f}")


