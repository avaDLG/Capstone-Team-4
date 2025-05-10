# Capstone-Team-4
University of Nebraska at Omaha code repository for Capstone Team 4 Spring 2025

# Code Milestone 5
1. Introduction:

 This application is an attempt to predict Computer Science class sizes for the University of Nebraska at Omaha. Every semester the CS administration must manually look at data from previous semesters to set the number of student spots avaliable for the upcoming semester. 
 
 For new users, you will need to register for a new account after choosing a type of login. You can put in any type of email and password at this point. After registration and login, you will see the home page of the tool where you can query class via the class code and select the Fall/Spring semester see the preliminary predictions from two regression models including Random Forest and Linear Regression. 
 
 The prediction results will also come with a note if a class is only offered in Fall/Spring or has been discontinued. If you want to run this app locally, you will have to make sure you have completed the step to authorize your device's connection to the database and have the file key.json and .env in the right location. More instruction can be found in the report. 

2. Release Notes:
 
 The application is built using the Flask web framework, with backend operations implemented in Python to interact with a MySQL database (hosted on Google Cloud), and frontend rendering handled through Jinja2 templates.
 
 Milestone 1 (M1): Initial setup. All elements that involved in development work were put together including this repository. 

Milestone 2 (M2): Finalized the exact data needed for model inputs and determined what kind of output that would be presented to users. Finished the fundamentals of a sign-in page and defined how the frontend should be formatted when having information from the backend. Multiple approaches and models of linear regression, multiple regression, ARIMA, etc. were explored. 

Milestone 3 (M3): The linear regression was fully developed with the frontend and back fully integrated. The routing between webpages of the system was refined and made fully functional for all required pages. Transitioned to a MySQL Database hosted on Google Cloud where more data of previous semester from farther back was created.

Milestone 4 (M4): A few initial system tests were created, and the frontend was finalized with updates to the sign-in process, added password hashing and the addition of plotted historical data visualizations for users to view trends alongside projections. Introduced the Random Forest (RF) Model. 

Milestone 5 (M5):  Testing was created to ensure the integrity of the system under multiple scenarios. The RF model is finalized. Finalized the webpage looks and displayed other information about the clas that can be powerful for users' decisions. 
 
3. Branches

 The 'main' branch has all of the work that we have pushed that does run sucessfully.
 
# Features
 
 🔐 Authenticated Login
 Secure login system for user access control.
 
 📈 Predictive Modeling
 Uses two regression models to forecast course enrollments with interpretive notes.
 
 📊 Historical Data Visualization
 Interactive charts and tables display past enrollment trends.
 
 🗃️ MySQL Database Integration
 Real-time querying and updating of academic data.
 
 🧩 Modular Backend Architecture
 Written in Python using Flask, supporting clean code separation and scalability
 
 🌐 Dynamic Frontend Rendering
 Jinja2 templates render intuitive and responsive interfaces.

