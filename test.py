import json 

with open('data/cs_enrollment.json', 'r') as f:
        cs_predictions = json.load(f)
        for subject, courses in cs_predictions.items():
            print(courses)
