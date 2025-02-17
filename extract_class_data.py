import json

# Load the JSON data from the file
with open('fa21-fa24.json') as f:
    data = json.load(f)

# List to store the extracted enrollment data
enrollment_data = []

# Loop through each course in the JSON file
for course_id, course_info in data.items():
    title = course_info.get('title', '')
    
    # Check if the course is CSCI or CIST
    if 'CSCI' in title or 'CIST' in title:
        # Loop through sections for each course
        for section_id, section_info in course_info.get('sections', {}).items():
            # Extract necessary details for each section
            section_data = {
                'course_id': course_id,
                'title': title,
                'section_id': section_id,
                'enrolled': int(section_info['Enrolled']),
                'class_max': int(section_info['Class Max']),
                'seats_available': int(section_info['Seats Available']),
                'instructor': section_info['Instructor'],
                'location': section_info['Location'],
                'time': section_info['Time'],
                'days': section_info['Days']
            }
            # Append to the list of enrollment data
            enrollment_data.append(section_data)

# Now, you can process or display the extracted enrollment data
for item in enrollment_data:
    print(item)

# Optional: Store the data in a CSV or DataFrame if needed for further analysis
# import pandas as pd
# df = pd.DataFrame(enrollment_data)
# df.to_csv('cs_courses_enrollment.csv', index=False)
