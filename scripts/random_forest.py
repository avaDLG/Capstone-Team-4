from flask import Flask, jsonify
import pandas as pd 
import numpy as np
import math
from sqlalchemy import text
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

def random_forest(session):
    """
    This function runs all class parameters with Random Forest Model.  
    param: db engine/session 
    return: None (for now)
    """
    
    # TODO: This would need to display the predictions/store it in the database 
    # The route /random_forest should be triggered to run this model, watch your console for results. 
    predictions = []
    
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

    # print(df) 

    # Fetch headcount
    hc_query = text("""
            SELECT Enrollment, Year, Semester FROM project_data.college_headcount 
            ORDER BY Year
        """)
    hc_result = session.execute(hc_query)
    hc_rows = hc_result.fetchall()
    hc_columns = hc_result.keys()  # Gets column names from the query

    df_headcount = pd.DataFrame(hc_rows, columns=hc_columns)
    # print(df_headcount)

    df_merged = pd.merge(
        df,
        df_headcount,
        on=["Year", "Semester"],  # Join keys
        how="left"
    )

    df_merged["Required"] = df_merged["Required"].astype(int)  # True/False → 1/0
    df_merged['Semester'] = df_merged['Semester'].map({'Fall': 0, 'Spring': 1})
    #df_merged = pd.get_dummies(df_merged, columns=["Semester"], drop_first=True)  # One-hot encode semester

    # print(df_merged)

    le = LabelEncoder()
    df_merged['Class_Code_encoded'] = le.fit_transform(df['Class_Code'])
    class_mapping = dict(enumerate(pd.Categorical(df_merged["Class_Code"]).categories))
    # print(class_mapping)

    X = df_merged[["Year", "Class_Code_encoded", "Enrollment_y", "Required", "Semester"]]  # features
    y = df_merged["Enrollment_x"]  # target

    # print(df_merged)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"RMSE: {mse**0.5:.2f}")
    print(f"R^2 Score: {r2:.2f}")

    scores = cross_val_score(model, X, y, scoring='neg_root_mean_squared_error', cv=5)
    print("Avg RMSE:", -scores.mean())
    
    # TODO: Fix this area to dynamically identify the class code etc. 
    data = {
    "Year": [2024],
    "Required": [1],  # or 0
    "Class_Code_encoded": [23], 
    "Enrollment_y": [1224],
    "Semester": [0]
    }

    df = pd.DataFrame(data)

    X_pred = df[["Year", "Class_Code_encoded", "Enrollment_y", "Required", "Semester"]]
    print(X_pred)
    prediction = model.predict(X_pred)

    print(f"Predicted Enrollment : {prediction[0]:.0f}")


