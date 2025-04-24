import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from config.config_db import engine  # Import database connection

# to make module on BOTH windows and Mac
import matplotlib
matplotlib.use('Agg') # matplotlib can only write to file
from matplotlib import pyplot as plt

def graph_data(class_code, sem):
    """
    This function fetches enrollment and headcount data from the database
    for the given class code and semester.
    Note: As this point, we assume we have a class code of the correct format 
    """

    # Create a session
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    # Query course enrollment data from the database
    # If the data is not available, return None as the file_name with an error message
    erll_available_years = []
    X2_vals = []
    try:
        enrollment_query = text("""
            SELECT Year, Enrollment FROM project_data.enrollment_data
            WHERE semester = :semester AND class_code = :class_code
            ORDER BY Year
        """)
        result = session.execute(enrollment_query, {"semester": sem, "class_code": class_code})
        rows = list(result)  # Cache the result

        X2_vals = [row.Enrollment for row in rows]
        erll_available_years = [row.Year for row in rows]
        print(X2_vals)
        print(erll_available_years)

        if not X2_vals:
            return (None, "Class code does not exist in our database. Do you mean something else?")
            
    except Exception as e:
        print("Error fetching enrollment data:", e)
        session.rollback()
        return
    finally:
        session.close()

    # If the code has made this far, it means there is enrollment data for that class_code
    # Grab the available_years and query the corresponding head_count  

    # Build the parameterized IN clause manually
    placeholders = ", ".join([f":y{i}" for i in range(len(erll_available_years))])
    params = {f"y{i}": y for i, y in enumerate(erll_available_years)}
    params["semester"] = sem 

    # Query headcount data from the database
    X1_vals = []
    try:
        sql = f"""
            SELECT Year, Enrollment FROM project_data.college_headcount 
            WHERE semester = :semester AND Year IN ({placeholders})
            ORDER BY Year
        """
        headcount_query = text(sql)

        result = session.execute(headcount_query, params)
        X1_vals = [row.Enrollment for row in result]

    except Exception as e:
        print("Error fetching headcount data:", e)
        session.rollback()
        return
       
    filename = f'{class_code.replace(" ", "")}_plot.png'

    try:
        with open(f'static/plots/{filename}'):
            pass 
    except FileNotFoundError:
        # Plot College Headcount
        plt.plot(erll_available_years, X1_vals, marker='o', linestyle='-', color='blue', label="Total College Headcount")

        # Plot Class Enrollment
        plt.plot(erll_available_years, X2_vals, marker='s', linestyle='--', color='red', label=f"Enrollment in {class_code}")

        # Labels and title
        plt.xlabel("Year")
        plt.ylabel("Count")
        plt.title(f"Headcount vs Enrollment Trend for {class_code} ({sem})")
        plt.legend()

        plt.savefig(f'static/plots/{filename}')    
        plt.close() 
        
    return (filename, "Successful!") 
