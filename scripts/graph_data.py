import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from config.config_db import engine  # Import database connection

def graph_data(class_code, sem):
    """
    This function fetches enrollment and headcount data from the database
    for the given class code and semester.
    """

    # Create a session
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    year_range = list(range(2010, 2024))

    # TODO: Srping 2025 data should be available 

    # Query headcount data from the database
    X1_vals = []
    try:
        headcount_query = text("""
            SELECT Year, Enrollment FROM project_data.college_headcount 
            WHERE semester = :semester
        """)
        result = session.execute(headcount_query, {"semester": sem})
        X1_vals = [row.Enrollment for row in result]

    except Exception as e:
        print("Error fetching headcount data:", e)
        session.rollback()
        return
       
    # Query course enrollment data from the database
    X2_vals = []
    try:
        enrollment_query = text("""
            SELECT Year, Enrollment FROM project_data.enrollment_data
            WHERE semester = :semester AND class_code = :class_code
        """)
        result = session.execute(enrollment_query, {"semester": sem, "class_code": class_code})
        X2_vals = [row.Enrollment for row in result]

    except Exception as e:
        print("Error fetching enrollment data:", e)
        session.rollback()
        return
    finally:
        session.close()

    # Ensure data consistency
    # if len(X_vals) != len(y_vals) or not X_vals:
    #     print("Error: Mismatched or empty data retrieved.")
    #     return

    # # Fit a regression line
    # m, b = np.polyfit(X_vals, y_vals, 1)  # Linear fit (y = mx + b)

    # Plot College Headcount
    plt.plot(year_range, X1_vals, marker='o', linestyle='-', color='blue', label="Total College Headcount")

    # Plot Class Enrollment
    plt.plot(year_range, X2_vals, marker='s', linestyle='--', color='red', label=f"Enrollment in {class_code}")

    # Labels and title
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.title(f"Headcount vs Enrollment Trend for {class_code} ({sem})")
    plt.legend()
    
    filename = ""
    try:
        with open(f'static/{class_code.replace(" ", "")}_plot.png'):
            pass 
    except FileNotFoundError:
        plt.savefig(f'static/{class_code.replace(" ", "")}_plot.png')             

    plt.close()
    filename = f'{class_code.replace(" ", "")}_plot.png'

    return filename
