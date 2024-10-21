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

def import_csv_to_db(csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)

        for row in reader:
            goal, level, kracht_oef, cardio_oef, days_per_week, schema, warming_up, stretching, strength_training, cardio, cooling_down = row
            
            # Create a new Fitnesschema record
            fitnesschema = Fitnesschema(
                goal=goal,
                level=level,
                kracht_oef=kracht_oef,
                cardio_oef=cardio_oef,
                number_of_days=int(days_per_week),
                type_of_schedule=schema,
                warming_up=warming_up if warming_up else None,
                stretching=stretching if stretching else None,
                strength_training=strength_training if strength_training else None,
                cardio=cardio if cardio else None,
                cooling_down=cooling_down if cooling_down else None
            )
            db.session.add(fitnesschema)
            db.session.commit()

            # Add exercises to the correct sections
            sections = {
                'warming_up': warming_up,
                'stretching': stretching,
                'strength_training': strength_training,
                'cardio': cardio,
                'cooling_down': cooling_down
            }
            
            for section_name, exercises_per_day in sections.items():
                if exercises_per_day:
                    days_exercises = exercises_per_day.split(') (')
                    days_exercises = [day.strip('() ') for day in days_exercises]

                    for day, exercise_ids in enumerate(days_exercises, start=1):
                        exercise_ids_list = [
                            int(ex_id.strip()) for ex_id in exercise_ids.split(',') if ex_id.strip().isdigit()
                        ]
                        
                        for order, exercise_id in enumerate(exercise_ids_list):
                            exercise_order = FitnesschemaExerciseOrder(
                                sportschema_id=fitnesschema.id,
                                section_name=section_name,
                                exercise_id=exercise_id,
                                exercise_order=order,
                                day=day
                            )
                            db.session.add(exercise_order)

            db.session.commit()


def import_csv_to_sets(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        
        for goal, level, warming_up_sets, stretching_sets, strength_training_sets, cardio_sets, cooling_down_sets, considerations in reader:
            # Create a new Sets object with data from the CSV
            new_set = Sets(
                goal=goal,
                level=level,
                warming_up_sets=warming_up_sets,
                stretching_sets=stretching_sets,
                strength_training_sets=strength_training_sets,
                cardio_sets=cardio_sets,
                cooling_down_sets=cooling_down_sets,
                considerations=considerations
            )
            # Add the new Sets object to the session
            db.session.add(new_set)
    
    # Commit the changes to the database
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
        import_csv_to_db("./csv_files/fitnesschemas.csv")
        import_csv_to_sets("./csv_files/sets.csv")
