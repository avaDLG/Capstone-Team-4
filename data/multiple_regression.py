# ava's second attempt at regression to predict cs class enrollment
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# Load JSON file
with open("data/CS_enrollment.json", "r") as file:
    data = json.load(file)