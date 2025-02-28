# Capstone-Team-4
University of Nebraska at Omaha code repository for Capstone Team 4 Spring 2025

# Code Milesone 1
1. Introduction:
This is an application to predict Computer Science class sizes for the University of Nebraska at Omaha. Every semester the CS administration must manually look at data from previous semesters to set the number of student spots avaliable for the upcoming semester. 

 To run the application locally run the app.py file and head http://127.0.0.1:5000/ The sign in page does not work ~yet~ but it will soon! You can see the UNO logo and future sign-in options. http://127.0.0.1:5000/regression is where you can see the regression model output (just in json format for now). And if you would like to filter by class .... http://127.0.0.1:5000/filter/CIST1400 use filter and the class code and number to be able to search for all data (past and predicted) for that specific class. 

2. Release Notes:
 
 The application is a currently an application of back-end linear regression modeling, a Flask API to connect to the the front end sign in screen.

The front end sign-in design is working, but the sign in is not yet. The ability to access the basic linear regression model and access past and future data by class from the web application running on local host is avaliable and working.

We will continue to refine and test new models, work on the sign in and authentication and display data in a better way. 
   
3. Branches

The Main branch has all of the work that we have pushed that does run sucessfully. The other branches we have are to keep developing the front and backend without interfereing with the basic model and interface we have now. They just hold our continuing work that will continue to be updated! '

ashley-test is Ashley's space to keep working on and designing the front end pages.

ava-testing is Ava's space to work on another regression model with multiple data inputs.

thi-feb26 is Thi's space to keep working on her models from the new UNO enrollment data we have found. 

