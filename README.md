# Capstone-Team-4
University of Nebraska at Omaha code repository for Capstone Team 4 Spring 2025

# Code Milestone 4
1. Introduction:

 This is an application to predict Computer Science class sizes for the University of Nebraska at Omaha. Every semester the CS administration must manually look at data from previous semesters to set the number of student spots avaliable for the upcoming semester. 
 
 To run the application locally run the app.py file and head http://127.0.0.1:5000/ You can see the UNO logo and the sign-in options. 
 
 After successful login, there should be a form to fill in the class code, select the Fall/Spring semester see the preliminary predictions. 

2. Release Notes:
 
 The application is a currently an application of back-end linear regression modeling, a Flask API to connect to the the front end HTML and CSS screens. 

 The sign-in functionality now supports all three types of logins and we add more frontend elements to make the class query form look more attractive to users. The logic that accounts for the users' input error is added for better user experience. Eg. csci3320 or CSCI3320 or csci 3320. If an invalid input is added, an error message will be displayed to let the user know the class code is incorrect. 

 On the model side, we add another route that triggers the Random Forest model. This route is still in progress and there is some area for improvement here. 

 The testing phase has started and will continue to be added.  
   
3. Branches

 The 'main' branch has all of the work that we have pushed that does run sucessfully. The other branches we have are to keep developing the front and backend without interfereing with the basic model and interface we have now. T

 ash_authentication - is Ashley's branch working with use authentication with username and passwords from the user side. 

 thi-linearmodels - an additional model is being developed. 

