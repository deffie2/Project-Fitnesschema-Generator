import os

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
from models import *

app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    """Display the homepage of the Fitness Schema Generator website."""
    return render_template("index.html")


@app.route("/info", methods=["POST"])
def info():
    """Here you can find information about fitness and fitness schedules."""
    return render_template('info.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":

        # Get username and password from the form
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if username and password are given, (No field left blank)
        if not username or not password:
            flash("Zowel gebruikersnaam als wachtwoord zijn vereist.", "error")
            return redirect(url_for("register"))

        # Confirm password matches the confirmation
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            flash("Wachtwoorden komen niet overeen", "error")
            return redirect(url_for("register"))

        # Check if username already exists in database
        if User.query.filter_by(username=username).first():
            flash("Gebruikersnaam bestaat al.", "error")
            return redirect(url_for("register"))

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create new user and add it to the database
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Flash a success message after successful registration
        flash("Registratie succesvol!", "success")

        # Redirect user to the homepage after successful registration
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":

        # Get username and password from the form
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Gebruikersnaam moet worden opgegeven.", "error")
            return redirect(url_for("index"))

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Wachtwoord moet worden opgegeven.", "error")
            return redirect(url_for("index"))

        # Query user from database
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if not user or not check_password_hash(user.password_hash, password):
            flash("Ongeldige gebruikersnaam en/of wachtwoord.", "error")
            return redirect(url_for("index"))

        # Set the username and id in the session
        session["user_id"] = user.id
        session["user_name"] = user.username

        # Redirect user to the homepage after successful login
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/fitnesschema_form", methods=["GET", "POST"])
@login_required
def fitnesschema_form():
    """Handle the submission and display of the fitnesschema form."""
    if request.method == "POST":
        # Retrieve the data submitted via the form
        goal = request.form.get("goal")
        level = request.form.get("level")
        kracht_oef = request.form.get("krachtOef")
        cardio_oef = request.form.get("cardioOef")
        days_per_week = request.form.get("days")
        schema = request.form.get("schema")

        # Check if all questions are answered
        if not all([goal, level, kracht_oef, cardio_oef, days_per_week, schema]):
            flash("Beantwoord alle vragen voordat je het schema genereert.", "info")
            return redirect(url_for("fitnesschema_form"))

        data = [goal, level, kracht_oef, cardio_oef, days_per_week, schema]

        # Process the form data
        schema_values = process_data(data)

        # Compare values and get fitnesschema id back
        schema_id = compare_schema_values(schema_values)

        # Check if no matching fitnesschema is found or if schema_id is a tuple
        if not schema_id or isinstance(schema_id, tuple):
            return apology("No matching fitnesschema gevonden", 400)

        # Get the current logged-in user's profile
        user_id = session.get("user_id")
        if not user_id:
            return apology("User not logged in", 400)

        # Retrieve the profile associated with the user_id from the database
        profile = Profile.query.filter_by(user_id=user_id).first()

        if not profile:
            flash("Maak eerst een profiel aan voordat je een fitnesschema kunt genereren.", "info")
            return redirect(url_for("profile"))

        # Check if the fitnesschema is already in the profile
        fitnesschema_in_profile = Fitnesschema.query.filter(
            Fitnesschema.id == schema_id,
            Fitnesschema.profiles.any(id=profile.id)
        ).first()

        # If the fitnesschema is not in the profile, add it
        if not fitnesschema_in_profile:
            fitnesschema = Fitnesschema.query.get(schema_id)
            if fitnesschema:
                profile.fitnesschemas.append(fitnesschema)
                db.session.commit()
            else:
                return apology("Fitnesschema niet gevonden.", 400)

        # Redirect to the function that handles displaying the fitnesschema
        return redirect(url_for('show_fitnesschema', id=schema_id))

    elif request.method == "GET":
        user_id = session.get('user_id')
        existing_profile = Profile.query.filter_by(user_id=user_id).first()

        if existing_profile:
            profile_found = True
        else:
            profile_found = False
        return render_template("fitnesschema_form.html", profile_found=profile_found)


def process_data(data):
    """Function to process the data from the from."""
    schema_values = []

    # Process goal
    schema_values.append(data[0])

    # Process level
    schema_values.append(data[1])

    # Process kracht_oef
    kracht_oef = data[2]
    if kracht_oef == "Combinatie van oefeningen met en zonder machines.":
        schema_values.append(0)
    elif kracht_oef == "Alleen oefeningen met machines.":
        schema_values.append(1)
    elif kracht_oef == "Alleen oefeningen zonder machines.":
        schema_values.append(2)
    elif kracht_oef == "Geen optie.":
        schema_values.append(3)

    # Process cardio_oef
    cardio_oef = data[3]
    if cardio_oef == "Combinatie van oefeningen met en zonder machines.":
        schema_values.append(0)
    elif cardio_oef == "Alleen oefeningen met machines.":
        schema_values.append(1)
    elif cardio_oef == "Alleen oefeningen zonder machines.":
        schema_values.append(2)

    # Process days_per_week
    schema_values.append(int(data[4]))

    # Process schema
    schema_values.append(data[5])

    return schema_values


def compare_schema_values(schema_values):
    """Compare the submitted schema values with existing fitnesschemas in the database."""
    # Ensure schema_values has the correct length
    if len(schema_values) != 6:
        return apology("Ongeldige invoergegevens.", 400)

    # Extract the values from the list
    goal = schema_values[0]
    level = schema_values[1]
    kracht_oef = schema_values[2]
    cardio_oef = schema_values[3]
    days_per_week = schema_values[4]
    type_of_schedule = schema_values[5]

    # Query the database for a fitnesschema that matches the submitted values
    matching_schema = Fitnesschema.query.filter(
        Fitnesschema.goal == goal,
        Fitnesschema.level == level,
        Fitnesschema.kracht_oef == kracht_oef,
        Fitnesschema.cardio_oef == cardio_oef,
        Fitnesschema.number_of_days == days_per_week,
        Fitnesschema.type_of_schedule == type_of_schedule
    ).first()

    # If a matching fitnesschema is found, return its ID.
    if matching_schema:
        return matching_schema.id
    else:
        return apology("Fitnesschema is niet gevonden", 400)


@app.route("/fitnesschema/<int:id>")
@login_required
def show_fitnesschema(id):
    """Display the details of a fitnesschema based on the given ID."""

    # Retrieve the fitnesschema based on the given ID
    fitnesschema = Fitnesschema.query.get(id)
    if not fitnesschema:
        return apology("Fitnesschema is niet gevonden", 400)

    # Initialize dictionaries to store exercises for different sections
    warming_up_exercises = {}
    stretching_exercises = {}
    strength_training_exercises = {}
    cardio_exercises = {}
    cooling_down_exercises = {}

    # Retrieve exercises for all days and sections of the fitnesschema
    for day in range(1, fitnesschema.number_of_days + 1):
        warming_up_exercises[day] = get_exercises_by_section_and_day(id, 'warming_up', day)
        stretching_exercises[day] = get_exercises_by_section_and_day(id, 'stretching', day)
        strength_training_exercises[day] = get_exercises_by_section_and_day(id, 'strength_training', day)
        cardio_exercises[day] = get_exercises_by_section_and_day(id, 'cardio', day)
        cooling_down_exercises[day] = get_exercises_by_section_and_day(id, 'cooling_down', day)

        # Format the instructions for each exercise
        for exercise in warming_up_exercises[day]:
            exercise.instructions = format_instructions(exercise.instructions)
            exercise.name = exercise.name.capitalize()
        for exercise in stretching_exercises[day]:
            exercise.instructions = format_instructions(exercise.instructions)
            exercise.name = exercise.name.capitalize()
        for exercise in strength_training_exercises[day]:
            exercise.instructions = format_instructions(exercise.instructions)
            exercise.name = exercise.name.capitalize()
        for exercise in cardio_exercises[day]:
            exercise.instructions = format_instructions(exercise.instructions)
            exercise.name = exercise.name.capitalize()
        for exercise in cooling_down_exercises[day]:
            exercise.instructions = format_instructions(exercise.instructions)
            exercise.name = exercise.name.capitalize()

    # Retrieve sets and all sets based on fitnesschema goal and level
    sets = get_sets(fitnesschema.goal, fitnesschema.level)
    all_sets = get_all_sets(fitnesschema.goal, fitnesschema.level)

    return render_template(
        "fitnesschema.html", 
        fitnesschema=fitnesschema, id=id,
        warming_up_exercises=warming_up_exercises,
        stretching_exercises=stretching_exercises,
        strength_training_exercises=strength_training_exercises,
        cardio_exercises=cardio_exercises,
        cooling_down_exercises=cooling_down_exercises,
        sets=sets,
        all_sets=all_sets
    )


def get_exercises_by_section_and_day(fitnesschema_id, section_name, day):
    """Retrieve exercises for a specific section and day of a fitnesschema."""
    exercises = db.session.query(Exercises_data).join(
        FitnesschemaExerciseOrder,
        Exercises_data.id == FitnesschemaExerciseOrder.exercise_id
    ).filter(
        FitnesschemaExerciseOrder.sportschema_id == fitnesschema_id,
        FitnesschemaExerciseOrder.section_name == section_name,
        FitnesschemaExerciseOrder.day == day
    ).all()

    # Iterate through each exercise and format its instructions if they are strings.
    for exercise in exercises:
        if isinstance(exercise.instructions, str):
            exercise.instructions = format_instructions(exercise.instructions)

    return exercises


def get_all_sets(goal, level):
    """Retrieve all sets based on goal and level."""
    sets = db.session.query(Sets).filter_by(goal=goal, level=level).all()
    return sets


def get_sets(goal, level):
    """Retrieve the first set based on goal and level."""
    sets = Sets.query.filter_by(goal=goal, level=level).first()
    return sets


def format_instructions(instructions):
    """Format the instructions to remove braces and split by comma."""
    # Check if instructions are a list containing a single string
    if isinstance(instructions, list) and len(instructions) == 1 and isinstance(instructions[0], str):
        # Extract the string from the list
        instructions = instructions[0]

    # Remove quotes at the beginning and end of the string
    instructions = instructions.strip('"')

    # Remove braces
    instructions = instructions.replace('{', '').replace('}', '')

    # Replace "," with an HTML line break
    instructions = instructions.replace('","', '<br>')
    return instructions


@app.route('/delete_fitnesschema/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_fitnesschema(id):
    # Retrieve the user's ID from the session
    user_id = session.get('user_id')

    # Find the user's profile
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        return apology("profiel niet gevonden.", 400)

    # Retrieve the profile's ID
    profile_id = profile.id

    # Find the fitness schema associated with the current profile and the provided fitnesschema_id
    fitnesschema = Fitnesschema.query.join(profile_fitnesschema_association).filter(
        profile_fitnesschema_association.c.profile_id == profile_id,
        Fitnesschema.id == id
    ).first()

    if not fitnesschema:
        return apology("Fitnesschema niet gevonden.", 400)

    if request.method == "POST":
        # Get the choice from the form
        choice = request.form.get("choice")
        if choice == "Ja":
            # Remove the association between the profile and the fitness schema
            profile.fitnesschemas.remove(fitnesschema)
            db.session.commit()
            flash("Fitness schema succesvol verwijderd.", "success")
            return redirect(url_for("profile"))
        elif choice == "Nee":
            flash("Verwijderen van fitnesschema geannuleerd.", "info")
            return redirect(url_for("profile"))

    return render_template("delete_fitnesschema.html", fitnesschema=fitnesschema, id=id, user_id=user_id, profile=profile)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Display and handle profile creation/update."""
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        weight = request.form.get("weight")
        height = request.form.get("height")
        experience_level = request.form.get("experience_level")
        goal = request.form.get("goal")
        goal_string = request.form.get("goal_string")

        # Convert empty strings to None for numeric fields
        age = age if age else None
        weight = weight if weight else None
        height = height if height else None

        # Validate age and weight fields
        if age is not None and not validate_age(age):
            return redirect(url_for("profile"))
        if weight is not None and not validate_weight(weight):
            return redirect(url_for("profile"))

        # Check if at least one field is filled
        if any([name, age, weight, height, experience_level, goal, goal_string]):
            # Gegevens opslaan in de sessie
            session["profile_data"] = {
                "name": name,
                "age": age,
                "weight": weight,
                "height": height,
                "experience_level": experience_level,
                "goal": goal,
                "goal_string": goal_string
            }
            print(session["profile_data"])
        else:
            flash("Vul tenminste één veld in!")
            return redirect(url_for("profile"))

        user_id = session.get('user_id')
        existing_profile = Profile.query.filter_by(user_id=user_id).first()
        # Render edit profile page if profile exists
        if existing_profile:
            return render_template("edit_profile.html", profile=existing_profile)

        # Create new profile if none exists
        profile = Profile(user_id=user_id, **session["profile_data"])
        db.session.add(profile)
        db.session.commit()
        flash("Profiel succesvol aangemaakt!", "success")
        return redirect(url_for("profile"))

    # Display profile page
    user_id = session.get('user_id')
    existing_profile = Profile.query.filter_by(user_id=user_id).first()

    if existing_profile:
        profile_found = True
        profile = existing_profile
    else:
        profile_found = False
        profile = None

    return render_template("profile.html", profile_found=profile_found, profile=profile)


def validate_age(age):
    """Validate age field."""
    try:
        age = int(age)
        if age < 18:
            flash("Leeftijd moet minimaal 18 jaar zijn.")
            return False
    except ValueError:
        flash("Leeftijd moet een numerieke waarde zijn.")
        return False
    return True


def validate_weight(weight):
    """Validate weight field."""
    try:
        weight = float(weight)
        if weight <= 0:
            flash("Gewicht moet een positieve waarde zijn.")
            return False
    except ValueError:
        flash("Gewicht moet een numerieke waarde zijn.")
        return False
    return True


@app.route("/edit_profile", methods=["POST", "GET"])
@login_required
def edit_profile():
    """Handle profile editing."""
    user_id = session.get('user_id')
    existing_profile = Profile.query.filter_by(user_id=user_id).first()

    if request.method == "POST":
        choice = request.form.get("choice")
        if choice == "Ja":
            profile_data = session.get("profile_data", {})

            if existing_profile:
                for key, value in profile_data.items():
                    # Update only if there's a new value
                    if value:
                        setattr(existing_profile, key, value)
                db.session.commit()
                flash("Profiel succesvol bijgewerkt!", "success")
        elif choice == "Nee":
             flash("Bewerking geannuleerd.", "info")

        # Remove profile data from session
        session.pop("profile_data", None)
        return redirect(url_for("profile"))

    return render_template("edit_profile.html", profile=existing_profile)


@app.route("/delete_profile", methods=["GET", "POST"])
@login_required
def delete_profile():
    """Handle profile deletion."""
    user_id = session.get('user_id')

    # Find the user's profile based on the user ID
    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile:
        flash("Profiel niet gevonden.")
        return redirect(url_for("profile"))

    if request.method == "POST":
        choice = request.form.get("choice")
        if choice == "Ja":
            db.session.delete(profile)
            db.session.commit()
            flash("Profiel succesvol verwijderd.", "success")
            return redirect(url_for("profile"))
        elif choice == "Nee":
            flash("Profiel verwijderen geannuleerd.", "info")
            return redirect(url_for("profile"))

    return render_template("delete_profile.html", profile=profile)


if __name__ == '__main__':
    app.run(debug=True)
