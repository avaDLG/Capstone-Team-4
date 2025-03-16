import json

def load_json_file(filename):
    '''
    This function iterates through the records in the json file and return a dictionary of course enrollment 
    param: json file path
    return: a dicitonary of course enrollment for CSCI and CIST classes 
    '''
    # load json file
    with open(filename) as f:
        data = json.load(f)

        course_enrollment = {}

        for term, subjects in data.items():
            for subject, courses in subjects.items():
                # for now only CS classes which have two codes
                if subject in ["CIST", "CSCI"]:  
                    for course_code, course_details in courses.items():
                        # only undergraduate classes --> cannot be above 5000 level
                        if int(course_code) <= 5000:  
                            # formatting "CIST 1300", "CSCI 1620"...
                            course_key = f"{subject} {course_code}"  

                            # make sure every class is acounted for 
                            if course_key not in course_enrollment:
                                course_enrollment[course_key] = {}

                            # interate through sections to find the year and semester
                            for section in course_details["sections"].values():
                                    
                                # DO NOT DOUBLE COUNT STUDENTS
                                if section["Type"] == "LAB":  # Ignore labs
                                    continue
                                date_range = section["Date"]
                                
                                # extract year and change month dates to fall or spring
                                year = date_range.split()[-1]  # Extract the year
                                
                                if "Aug" in date_range or "Sep" in date_range:
                                    semester = "Fall"
                                elif "Jan" in date_range or "Feb" in date_range:
                                    semester = "Spring"
                                else:
                                    continue  # TEST THIS!!!

                                # Ensure the year exists in the dictionary
                                if semester not in course_enrollment[course_key]:
                                    course_enrollment[course_key][semester] = {}

                                if year not in course_enrollment[course_key][semester]:
                                    course_enrollment[course_key][semester][year] = 0

                                # Add enrollment to the correct semester
                                course_enrollment[course_key][semester][year] += int(section["Enrolled"])

    # print(json.dumps(course_enrollment, indent=4))
    return course_enrollment

def write_json_file(course_enrollment: dict):
    '''
    This function takes in a dictionary and writes it to a file 
    param: a dictionary of course enrollment 
    return: None 
    '''
    with open("data/cs_enrollment.json", "w") as f:
        json.dump(course_enrollment, f, indent=4)

if __name__ == "__main__": 
    course_enrollment = dict()
    course_enrollment = load_json_file("data/cist_csci_fall11_fall24.json")
    #print(course_enrollment)
    write_json_file(course_enrollment)


