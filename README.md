# Capstone-Team-4
University of Nebraska at Omaha code repository for Capstone Team 4 Spring 2025

# Code Milesone 3
1. Introduction:

 This is an application to predict Computer Science class sizes for the University of Nebraska at Omaha. Every semester the CS administration must manually look at data from previous semesters to set the number of student spots avaliable for the upcoming semester. 
 
 To run the application locally run the app.py file and head http://127.0.0.1:5000/ You can see the UNO logo and the sign-in options. 
 
 After successful login, there should be a form to fill in the class code, select the Fall/Spring semester see the preliminary predictions. 

2. Release Notes:
 
 The application is a currently an application of back-end linear regression modeling, a Flask API to connect to the the front end HTML and CSS screens. 

 The sign-in functionality is working with password hashing and user registration. After registration, users should be able to use their just registered credentials to log in. You can view the details about a particular class with the correct code. 

 While the model remains the same, the backend design evolves with the MySQL database hosted on Google Cloud. Related information about a class is now centralized and displayed on the result page. 

 Documentation from Doxygen has been configured to work with the code. 
   
3. Branches

 The Main branch has all of the work that we have pushed that does run sucessfully. The other branches we have are to keep developing the front and backend without interfereing with the basic model and interface we have now. T

 ash_authentication - is Ashley's branch working with use authentication with username and passwords from the user side. 

 ava-docs - is Ava's branch to learn how to use Doxy and create the HTML documentation page correctly.

 thi-database-integration - has been pulled to the main branch for database integration and refactoring. 

