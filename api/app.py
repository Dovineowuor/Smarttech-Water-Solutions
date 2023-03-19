from flask import Flask, request
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
import pymongo

# Initialize the Flask application
app = Flask(__name__)

# Initialize PyMongo to connect to MongoDB server
app.config['MONGO_URI'] = 'mongodb://localhost:27017/powerhacks_water_solution'
mongo = PyMongo(app)

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize JWT for authentication
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)


# Define the data models for the API using Python classes.
# User class with attributes like name, email, and password
class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


# Water usage class
class WaterUsage:
    def __init__(self, user_id, gallons_used, date):
        self.user_id = user_id
        self.gallons_used = gallons_used
        self.date = date


# Leaks class
class Leak:
    def __init__(self, user_id, location, date_reported):
        self.user_id = user_id
        self.location = location
        self.date_reported = date_reported


# Water quality class
class WaterQuality:
    def __init__(self, user_id, ph_level, chlorine_level, date_tested):
        self.user_id = user_id
        self.ph_level = ph_level
        self.chlorine_level = chlorine_level
        self.date_tested = date_tested


# Analytics class
class Analytics:
    def __init__(self, user_id, analytics_type, data, date_generated):
        self.user_id = user_id
        self.analytics_type = analytics_type
        self.data = data
        self.date_generated = date_generated


# Implement user authentication and authorization using a library like Flask-Login or Flask-JWT.
# Create endpoints for user login and registration.
@app.route('/register', methods=['POST'])
def register():
    # Get user input from the request
    name = request.json['name']
    email = request.json['email']
    password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')

    # Check if user already exists in the database
    if mongo.db.users.find_one({'email': email}):
        return {'message': 'User already exists'}, 409

    # Add the user to the database
    user_id = mongo.db.users.insert({'name': name, 'email': email, 'password': password})
    return {'message': 'User created successfully', 'user_id': str(user_id)}, 201


@app.route('/login', methods=['POST'])
def login():
    # Get user input from the request
    email = request.json['email']
    password = request.json['password']

    # Check if user exists in the database
    user = mongo.db.users.find_one({'email': email})
    if not user:
        return {'message': 'Invalid email or password'}, 401

    # Check if password is correct
    if not bcrypt.check_password_hash(user['password'], password):
        return {'message': 'Invalid email or password'}, 401

    # Create an access token for the user
    access_token = create_access_token(identity=str(user['_id']))
    return {'access_token': access_token}, 200


# Define the endpoints for the API using a Python web framework
