from flask import Flask, jsonify
from sqlalchemy import text
from datetime import datetime
import numpy as np 
import pandas as pd 

from sklearn.metrics import r2_score
from sklearn.metrics import root_mean_squared_error

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Function to run Linear Regression and predict enrollments
def linear_regression_run(session, semester):
    """
    This function takes in the semester and run a linear regression for enrollment predictions of the class. 
    param: db engine/session, semester Fall/Spring 
    return: a dictionary of new predictions that are just added to the db  
    """
    predictions_df = pd.DataFrame(columns=["class_code", "year", "semester", "predicted_enrollment", "note"])
    COVID_YEAR = 2020

    # Fetch course enrollment data
    course_data_query = text("""
                        SELECT class_code, year, enrollment 
                        FROM project_data.enrollment_data 
                        WHERE semester = :semester AND enrollment > 0
                        ORDER BY year 
                        """)
    result = session.execute(course_data_query, {"semester": semester})
    rows = result.fetchall()
    columns = result.keys()  # Gets column names from the query

    course_enrollment_df = pd.DataFrame(rows, columns=columns)
    course_enrollment_df['year_offset'] = course_enrollment_df['year'] - 2020
    # print(course_enrollment_df)

    # Fetch headcount data
    headcount_query = text("""SELECT year, enrollment 
                           FROM college_headcount 
                           WHERE semester = :semester
                           """)
    hc_result = session.execute(headcount_query, {"semester": semester})
    hc_rows = hc_result.fetchall()
    hc_columns = hc_result.keys() 

    headcount_df = pd.DataFrame(hc_rows, columns=hc_columns)
    headcount_df['year_offset'] = headcount_df['year'] - COVID_YEAR
    # print(headcount_df)

    class_codes_list = course_enrollment_df['class_code'].unique().tolist()
    now = datetime.now()
    if now.month >= 8:  # August or later → Fall already started
        next_year = now.year + 1
    else:
        next_year = now.year

    # Loop through each class (using class_code)
    for class_code in class_codes_list:
        
        X = []  # Current feature: [Headcount, Years with Covid as baseline]
        y = []  # Target: Enrollment

        # Filter the course data for the current class_code
        filtered_df = course_enrollment_df[course_enrollment_df['class_code'] == class_code]
        latest_offering = filtered_df.iloc[-1]
        current_year = datetime.now().year 

        # Assuming we would only care about classes that are offered within 5 years  
        if abs(latest_offering["year"]-current_year) >= 5: 
            # this class has not been offered for 5 years or more
            new_pred = pd.DataFrame([{
                "class_code": class_code,
                "year": next_year,
                "semester": semester,
                "predicted_enrollment": 0, 
                "note": "not offered within 5 years"
            }])
            predictions_df = pd.concat([predictions_df, new_pred], ignore_index=True)
        
        else: 
            # this class was offered in the past 5 years
            if len(filtered_df) < 4: 
                # does not have enough data 
                new_pred = pd.DataFrame([{
                    "class_code": class_code,
                    "year": next_year,
                    "semester": semester,
                    "predicted_enrollment": f"{latest_offering["enrollment"]}", 
                    "note": "not enough data for the model, use the most recent year data"
                }])
                predictions_df = pd.concat([predictions_df, new_pred], ignore_index=True)
            else: 
                # enough data to build the model 
                merged_df = filtered_df.merge(headcount_df, on=["year", "year_offset"])
                print(merged_df)
                # set up the model 
                X = merged_df[["year_offset", "enrollment_y"]]
                y = merged_df["enrollment_x"]
                # print(X,y)
        
                # Split data into training and test sets
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, shuffle=False 
                )  

                # Set up the LR model 
                model = LinearRegression()
                model.fit(X_train, y_train)

                r2 = r2_score(y_train, model.predict(X_train))
                if r2 < 0.3:
                    print(f"[SKIP] {class_code}: Poor fit (R²={r2:.2f})")
                    continue
                else:
                    print(f"[KEEP] {class_code}: Acceptable fit (R²={r2:.2f})")
                    # rmse = root_mean_squared_error(y_test, model.predict(X_test))
                    # print(f"RMSE: {rmse:.2f}")

            # Predict enrollment for the next year
            if next_year not in headcount_df["year"]:
                print(f"No headcount data available for {next_year}, running interpolate.")
            
                # Append missing year with NaN headcount
                new_row = pd.DataFrame([{
                    "year": next_year,
                    "year_offset": next_year - 2020,
                    "enrollment": np.nan
                }])
                headcount_df = pd.concat([headcount_df, new_row], ignore_index=True)

                # Sort and interpolate
                headcount_df = headcount_df.sort_values("year").reset_index(drop=True)
                headcount_df["enrollment"] = headcount_df["enrollment"].interpolate(method='linear')
            
            # Retrieve interpolated or existing headcount
            next_headcount = headcount_df.loc[headcount_df["year"] == next_year, "enrollment"].values[0]
            next_offset = next_year - 2020

            # Build prediction input
            X_pred = pd.DataFrame([{
                "year_offset": next_offset,
                "enrollment_y": next_headcount
            }])

            # Predict enrollment for the next year
            predicted_enrollment = model.predict(X_pred)[0]
            predicted_enrollment = max(0, round(predicted_enrollment))  # Ensure no negative predictions
            print(f"Predicted enrollment for {class_code} in {next_year}: {predicted_enrollment}") 

            new_pred = pd.DataFrame([{
                "class_code": class_code,
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
                INSERT INTO predictions (class_code, year, semester, predicted_enrollment, note)
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
