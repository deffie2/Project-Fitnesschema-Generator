import csv
import os

import requests

from flask import Flask, render_template, request
from models import *

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

#Function to retrieve data from exercise database  
def retrieve_data_from_exercise_db(bodyPart):
    base_url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/"
    
    bodypart_urls = {
        "back": "back",
        "cardio": "cardio",
        "chest": "chest",
        "lower arms": "lower%20arms",
        "lower legs": "lower%20legs",
        "neck": "neck",
        "shoulders": "shoulders",
        "upper arms": "upper%20arms",
        "upper legs": "upper%20legs",
        "waist": "waist"
    }

    # Check if the provided body part is in the dictionary
    if bodyPart in bodypart_urls:
        url = base_url + bodypart_urls[bodyPart]

        # Parameters for the API request
        querystring = {"limit":"250"}

        # Headers for the API request
        headers = {
        "X-RapidAPI-Key": "2281aabb27msh1f1cabb42551e22p1ed699jsncd475c0c6878",
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
        }

        # Make a GET request to the API
        response = requests.get(url, headers=headers, params=querystring)

        # Check if the request was successful
        if response.status_code == 200:
            databexercercises = response.json()

            # Iterate through the exercise data and add to the database
            for data in databexercercises:
                data_obj = Exercises_data(
                    bodyPart=data['bodyPart'],
                    name=data['name'],
                    target=data['target'],
                    equipment=data['equipment'],
                    instructions=data['instructions'],
                    gifUrl=data['gifUrl']
                )
                db.session.add(data_obj)

            # Commit changes to the database
            db.session.commit()
            return True
        else:
            # Handle errors if the request fails
            return False
    else:
        # Handle invalid bodypart
        print("Invalid bodyPart:", bodyPart)
        return False

if __name__ == "__main__":
    with app.app_context():
        body_parts = [
            "back", "cardio", "chest", "lower arms", "lower legs",
            "neck", "shoulders", "upper arms", "upper legs", "waist"]
        # Call the retrieve_data_from_exercise_db function for each body part

        for parts in body_parts:
            retrieve_data_from_exercise_db(parts)
