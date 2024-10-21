from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Stores user information."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    profile = db.relationship("Profile", uselist=False, back_populates="user")


# Intermediate class for the many-to-many relationship between Profile and Fitnesschema
profile_fitnesschema_association = db.Table('profile_fitnesschema_association',
    db.Column('profile_id', db.Integer, db.ForeignKey('profiles.id')),
    db.Column('fitnesschema_id', db.Integer, db.ForeignKey('fitnesschemas.id'))
)


class Profile(db.Model):
    """Stores user profile information."""
    __tablename__ = "profiles" 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100))
    age = db.Column(db.String(10))
    weight = db.Column(db.String(10))
    height = db.Column(db.String(10))
    experience_level = db.Column(db.String(50))
    goal = db.Column(db.String(50))
    goal_string = db.Column(db.String(100))
    user = db.relationship("User", back_populates="profile")
    fitnesschemas = db.relationship('Fitnesschema', secondary='profile_fitnesschema_association', back_populates='profiles')


class Exercises_data(db.Model):
    """Stores information about exercises."""
    __tablename__ = "exercises_data"
    id = db.Column(db.Integer, primary_key=True)
    bodyPart = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    target = db.Column(db.String, nullable=False)
    equipment = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    gifUrl = db.Column(db.String, nullable=False)


class Fitnesschema(db.Model):
    """Stores fitness schema information."""
    __tablename__ = "fitnesschemas"
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    level = db.Column(db.String, nullable=False)
    kracht_oef = db.Column(db.Integer, nullable=False)
    cardio_oef = db.Column(db.Integer, nullable=False)
    number_of_days = db.Column(db.Integer, nullable=False)
    type_of_schedule = db.Column(db.String, nullable=False)
    warming_up = db.Column(db.String, nullable=True)
    stretching = db.Column(db.String, nullable=True)
    strength_training = db.Column(db.String, nullable=True)
    cardio = db.Column(db.String, nullable=True)
    cooling_down = db.Column(db.String, nullable=True)
    fitnesschema_exercise_orders = db.relationship('FitnesschemaExerciseOrder', backref='fitnesschema', lazy=True)
    profiles = db.relationship('Profile', secondary='profile_fitnesschema_association', back_populates='fitnesschemas')
    

    def __init__(self, goal, level, kracht_oef, cardio_oef, number_of_days, type_of_schedule, warming_up=None, stretching=None, strength_training=None, cardio=None, cooling_down=None):
        self.goal = goal
        self.level = level
        self.kracht_oef = kracht_oef
        self.cardio_oef = cardio_oef
        self.number_of_days = number_of_days
        self.type_of_schedule = type_of_schedule
        self.warming_up = warming_up
        self.stretching = stretching
        self.strength_training = strength_training
        self.cardio = cardio
        self.cooling_down = cooling_down


class FitnesschemaExerciseOrder(db.Model):
    __tablename__ = "fitnesschema_exercise_order"
    """Stores the order of exercises in a fitness schema."""
    id = db.Column(db.Integer, primary_key=True)
    sportschema_id = db.Column(db.Integer, db.ForeignKey('fitnesschemas.id'))
    section_name = db.Column(db.String, nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises_data.id'))
    exercise_order = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    exercise = db.relationship("Exercises_data", backref="fitnesschema_exercise_orders")


class Sets(db.Model):
    """Stores sets information."""
    __tablename__ = "sets"
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    level = db.Column(db.String, nullable=False)
    warming_up_sets = db.Column(db.String, nullable=True)
    stretching_sets = db.Column(db.String, nullable=True)
    strength_training_sets = db.Column(db.String, nullable=True)
    cardio_sets = db.Column(db.String, nullable=True)
    cooling_down_sets = db.Column(db.String, nullable=True)
    considerations = db.Column(db.String, nullable=False)


    def __init__(self, goal, level, considerations, warming_up_sets=None, stretching_sets=None, strength_training_sets=None, cardio_sets=None, cooling_down_sets=None):
        self.goal = goal
        self.level = level
        self.warming_up_sets = warming_up_sets
        self.stretching_sets = stretching_sets
        self.strength_training_sets = strength_training_sets
        self.cardio_sets = cardio_sets
        self.cooling_down_sets = cooling_down_sets
        self.considerations = considerations 
