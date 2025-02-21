import json

# Load the JSON data from the file
with open('fa21-fa24.json') as f:
    data = json.load(f)

    course_enrollment = {}

    for term, subjects in data.items():
        for subject, courses in subjects.items():
            if subject in ["CIST", "CSCI"]:  # Filtering only CIST and CSCI subjects
                for course_code, course_details in courses.items():
                    if int(course_code) <= 5000:  # Only courses with code ≤ 5000
                        course_key = f"{subject} {course_code}"  # Format "CIST 1300", "CSCI 1620", etc.

                        # Initialize course entry if not present
                        if course_key not in course_enrollment:
                            course_enrollment[course_key] = {}

                        # Iterate through sections to extract year and semester from "Date"
                        for section in course_details["sections"].values():
                            date_range = section["Date"]
                            
                            # Extract year and determine semester
                            year = date_range.split()[-1]  # Extract the year
                            
                            if "Aug" in date_range or "Sep" in date_range:
                                semester = "Fall"
                            elif "Jan" in date_range or "Feb" in date_range:
                                semester = "Spring"
                            else:
                                continue  # Skip if the date isn't clear

                            # Ensure the year exists in the dictionary
                            if year not in course_enrollment[course_key]:
                                course_enrollment[course_key][year] = {"Fall": 0, "Spring": 0}

                            # Add enrollment to the correct semester
                            course_enrollment[course_key][year][semester] += int(section["Enrolled"])

# Print the result
print(json.dumps(course_enrollment, indent=4))


