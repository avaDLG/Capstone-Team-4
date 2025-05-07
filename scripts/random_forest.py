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

def random_forest(session, semester):
    """
    This function runs all class parameters with Random Forest Model.  
    param: db engine/session, semester Fall/Spring 
    return: a dictionary of new predictions made from the model 
    """
    
    predictions_df = pd.DataFrame(columns=["class_code", "year", "semester", "predicted_enrollment", "note"])
    
    # Fetch course enrollment data
    erll_query = text("""
        SELECT Class_Code, Class_Name, Year, Semester, Enrollment, Required
        FROM project_data.enrollment_data
        WHERE Enrollment > 0
        ORDER BY year 
    """)

    result = session.execute(erll_query)
    rows = result.fetchall()
    columns = result.keys()
    course_enrollment_df = pd.DataFrame(rows, columns=columns)
    # print(course_enrollment_df) 

    # Fetch headcount
    hc_query = text("""
            SELECT Enrollment, Year, Semester FROM project_data.college_headcount 
            ORDER BY Year
        """)
    hc_result = session.execute(hc_query)
    hc_rows = hc_result.fetchall()
    hc_columns = hc_result.keys() 
    headcount_df = pd.DataFrame(hc_rows, columns=hc_columns)

    merged_df = pd.merge(
        course_enrollment_df,
        headcount_df,
        on=["Year", "Semester"],  # Join keys
        how="left"
    )

    # Convert Categorical data to Numeric data 
    merged_df["Required"] = merged_df["Required"].astype(int)  # True/False → 1/0
    merged_df['Semester'] = merged_df['Semester'].map({'Fall': 0, 'Spring': 1})
    # print(merged_df)

    le = LabelEncoder()
    merged_df['Class_Code_encoded'] = le.fit_transform(merged_df['Class_Code'])
    # class_mapping is a key-value pair that key is the encoded and value is the class name
    class_mapping = dict(enumerate(pd.Categorical(merged_df["Class_Code"]).categories))
    # keep track of all classes - TODO: Should this be the class index?
    list_all_classes = list(class_mapping.values())

    # Build the Model 
    X = merged_df[["Year", "Class_Code_encoded", "Enrollment_y", "Required", "Semester"]]  # features
    y = merged_df["Enrollment_x"]  # target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # Some metrics about the result 
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"RMSE: {mse**0.5:.2f}")
    print(f"R^2 Score: {r2:.2f}")
    scores = cross_val_score(model, X, y, scoring='neg_root_mean_squared_error', cv=5)
    print("Avg RMSE:", -scores.mean())
    # End of metrics 

    if semester == "Fall":
        sem_param = [0]
    else: 
        sem_param = [1]

    # Get the next year for prediction 
    now = datetime.now()
    if now.month >= 8:  # August or later → Fall already started
        next_year = now.year + 1
    else:
        next_year = now.year

    headcount_per_sem = headcount_df[headcount_df["Semester"] == semester]
    # Predict enrollment for the next year
    if next_year not in headcount_per_sem["Year"]:
        
        # Append missing year with NaN headcount
        new_row = pd.DataFrame([{
            "Year": next_year,
            "Enrollment": np.nan
        }])
        headcount_per_sem = pd.concat([headcount_per_sem, new_row], ignore_index=True)

        # Sort and interpolate
        headcount_per_sem = headcount_per_sem.sort_values("Year").reset_index(drop=True)
        headcount_per_sem["Enrollment"] = headcount_per_sem["Enrollment"].interpolate(method='linear')

    next_headcount = headcount_per_sem.loc[headcount_per_sem["Year"] == next_year, "Enrollment"].values[0]

    print(next_headcount)
    # Run predictions for all classes  
    for one_class in list_all_classes:

        filtered_df = merged_df.loc[(merged_df['Semester'] == sem_param[0]) & (merged_df['Class_Code'] == one_class)]

        # if the df is empty, it means the class has never been offered in this particular semester
        if filtered_df.empty:
            new_pred = pd.DataFrame([{
                "class_code": one_class,
                "year": next_year,
                "semester": semester,
                "predicted_enrollment": [0], 
                "note": f"has never been offered in {semester}"
            }])
        else:
            # we are good to proceed... 

            # if a class does not have enough data
            # still make a prediction but with a note 
            class_encoded = [key for key, val in class_mapping.items() if val == one_class]
            
            required = filtered_df["Required"].iloc[0]
            data = {
                "Year": [next_year],
                "Required": [required], 
                "Class_Code_encoded": class_encoded, 
                "Enrollment_y": [next_headcount],
                "Semester": sem_param
            }

            features_df = pd.DataFrame(data)
            X_pred = features_df[["Year", "Class_Code_encoded", "Enrollment_y", "Required", "Semester"]]
            predicted_enrollment = model.predict(X_pred)[0]
            predicted_enrollment = max(0, round(predicted_enrollment))

            if len(filtered_df) < 4:   
                # does not have enough data 
                new_pred = pd.DataFrame([{
                    "class_code": one_class,
                    "year": next_year,
                    "semester": semester,
                    "predicted_enrollment": predicted_enrollment, 
                    "note": f"limited data - {len(filtered_df)}"
                }])
            else: 
                # valid data 
                new_pred = pd.DataFrame([{
                    "class_code": one_class,
                    "year": next_year,
                    "semester": semester,
                    "predicted_enrollment": predicted_enrollment, 
                    "note": "predicted from the model"
                }])
        predictions_df = pd.concat([predictions_df, new_pred], ignore_index=False)

    # Insert query 
    for _, row in predictions_df.iterrows():
        session.execute(
            text("""
                INSERT INTO rr_predictions (class_code, year, semester, predicted_enrollment, note)
                VALUES (:class_code, :year, :semester, :predicted_enrollment, :note)
                ON DUPLICATE KEY UPDATE
                    predicted_enrollment = :predicted_enrollment,
                    note = :note 
            """),
            {
                "class_code": row["class_code"],
                "year": row["year"],
                "semester": row["semester"],
                "predicted_enrollment": row["predicted_enrollment"],
                "note": row["note"]
            }
        )
    session.commit()
    print("Predictions saved successfully.")
    return predictions_df.to_dict(orient='records')

        
