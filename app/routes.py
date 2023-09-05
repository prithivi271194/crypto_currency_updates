"""
All routes for the application are defined here.

This module defines various routes for the application. Each route serves a specific purpose
and is described briefly below.

Routes:
    - `/v1/public/register`: Register page.
    - `/v1/public/login`: Login page.
    - `/v1/private/logout`: Logout page.
    - `/v1/private/summary`: To list the overall summary page
    - `/v1/private/<market>/summary`: To list the particular markert summary page.
"""


from functools import wraps
from datetime import datetime, timedelta
import re
import json
import requests
import jwt
from flask import Blueprint, jsonify, Response, request, current_app
from flask_login import login_user, logout_user
from app.models import db, User
from app import login_manager

# Create a blueprint for the API
api_bp = Blueprint('api', __name__)

def token_required(function):
    """
        This decorator function is to validate the user authentication
        for the private endpoints.
        If authentication is successfully, then call the route function with the required arguments.
        else return the Authentication error - 401.
    """
    @wraps(function)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = data['username']
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as err:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(err)
            }, 500
        return function(*args, **kwargs)
    return decorated


def get_user_from_database(username):
    """
        This function will basically get the userdetails from the database.
        
        Input : username
        If user not found in the user table then raise exception.
    """
    try :
        user = User.query.filter_by(username=username).first()
    except Exception as err:
        raise err
    user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password
        }
    return (user, user_data)


@api_bp.route('/apidocs')
def swagger():
    """
    Get an Swagger documentation UI
    ---
    responses:
      200:
        description: A successful response
    """
    return jsonify({'message': 'Swagger Version - 2.0'})


@api_bp.route('/v1/public/register', methods=['POST'])
def user_registration():
    """
    User Registration
    ---
    tags:
      - Registration
    summary: Register user details for the application
    description: Register user details in the database.
    consumes:
      - application/json
    parameters:
      - in: body
        name: user
        description: User deatils for registration.
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: User's username.
              example: admin
            password:
              type: string
              description: User's password.
              example: secretpassword
            email:
              type: string
              description: User's email ID.
              example: flask_admin@gmail.com
    responses:
      200:
        description: Successful login
        schema:
          type: object
          properties:
            message:
              type: string
              description: Successfull message
              example: Registration successfull
      400:
        description: Registration failed
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message for registration.
              example: Registration failed, Please try again later.

"""
    data = request.get_json()
    exception = False
    if data is None:
        return jsonify({'message': 'Invalid request. JSON data required.'}), 400
    if data and 'username' in data and 'password' in data and 'email' in data:
        user_name = data['username']
        pass_word = data['password']
        email_id = data['email']
        if user_name and pass_word and email_id:
            try:
                user = User(username=user_name, password=pass_word, email=email_id)
                db.session.add(user)
                db.session.commit()
            except Exception as err:
                exception = True
            if exception is True:
                return jsonify({'Message': 'Exception while inserting record in database,'
                                'User details already exists in table.'}), 400
            return jsonify({'message': 'User registered successfully'}), 200
    return jsonify({'message': 'Insufficient information.'
                                'Please check and provide proper inputs.'}), 400


@api_bp.route('/v1/public/login', methods=['POST'])
def login():
    """
    User Login
    ---
    tags:
      - Authentication
    summary: Login to the application
    description: Login to the application using username and password.
    consumes:
      - application/json
    parameters:
      - in: body
        name: user
        description: User credentials for login.
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: User's username.
              example: prithiviraj
            password:
              type: string
              description: User's password.
              example: secretpassword
    responses:
      200:
        description: Successful login
        schema:
          type: object
          properties:
            message:
              type: string
              description: Successfull Message and Authentication token.
              example: Login successfull and Token <HashValue>
      401:
        description: Unauthorized
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message for unauthorized login.
              example: Login failed. Check your credentials.
    """
    data = request.get_json()
    if data is None:
        return jsonify({'message': 'Invalid request. JSON data required.'}), 400
    secret_key = current_app.config['SECRET_KEY']
    if data and 'username' in data and 'password' in data:
        username = data['username']
        password = data['password']
        data['exp'] = datetime.utcnow() + timedelta(minutes = 30)

        # Check if the username exists in the user database
        try:
            (user_obj, user) = get_user_from_database(username)
        except Exception as err:
            user = None
        if user is None:
            return jsonify({'Message': 'Login failed.'
                                        'Unable to find the User details in Database.'
                                        'Please contact admin'}), 401
        if username == user["username"] and user["password"] == password:
            # Log the user in
            login_user(user_obj)
            token = jwt.encode(data, secret_key, algorithm="HS256")
            return jsonify({'Message': 'Login successful', 'AuthToken': token})
    return jsonify({'Message': 'Login failed. Check your credentials.'}), 401

@api_bp.route('/v1/private/protected')
@token_required
def protected_route():
    """
        This function is to ensure the enpoint is protected with authentication.
        If authentication is successfull then return This route is protected. 
    """
    return jsonify({'Message': 'This route is protected.'})


@api_bp.route('/v1/private/logout', methods=['GET'])
@token_required
def logout():
    """
        This function is to logout the current user.
    """
    logout_user()
    return jsonify({'Message': 'Logged out'})


@login_manager.user_loader
def load_user(user_id):
    """
        This is the logic to load a user from the user database based on user_id
    """
    return User.query.get(int(user_id))


@api_bp.route('/v1/private/summary', methods=['GET'])
@token_required
def overall_summary():
    """
    Get the overall Market Summary
    ---
    tags:
      - Overall Summary
    summary: Get all the Market Cryto Currency status
    description: Will retrive Cryto Currency summary for all companies.
    responses:
      200:
        description: Successful response
        schema:
          type: object
          properties:
            message:
              type: string
              description: Overall market summary in the json format
              example: JSON 
      404:
        description: Unable to retrive the data
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating that unable to fetch the summary
              example: Unable to retrive the overall summary
    """
    home_page = current_app.config['PARENT_API']
    timeout_seconds = 10
    data = requests.get(home_page, timeout=timeout_seconds)
    exception = False
    if data.status_code == 200:
        markets_summary = current_app.config['OVERALL_SUMMARY_API']
        try:
            summary = requests.request("GET", markets_summary, timeout=timeout_seconds)
            summary = summary.json()
        except Exception as err:
            exception = True
        if exception is True:
            return jsonify({'message': 'Unable to retrive the overall summary'})
        response = Response(
                response=json.dumps(summary),
                status=200,
                mimetype='application/json'
        )
        return response
    return jsonify({'message': 'Unable to retrive the overall summary'})


@api_bp.route('/v1/private/<company>/summary')
@token_required
def market_summary(company):
    """
    Get the Specific market Summary
    ---
    tags:
      - Market Summary
    summary: Get a particular market cryto currency status
    description: Will retrive Cryto Currency summary for the given company.
    parameters:
      - in: path
        name: company
        type: string
        description: Name of the company.
        required: true
        example: 1ECO-USDT
    responses:
      200:
        description: Successful response
        schema:
          type: object
          properties:
            message:
              type: string
              description: Particular market summary in the json format
              example: JSON
      404:
        description: Unable to retrive the data
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating that error in fetching the summary
              example: Unable to retrive the market summary
    """
    exception = False
    timeout_seconds = 10
    if company is not None:
        company = str(company)
        company_summary_api = current_app.config['MARKET_SUMMARY_API']
        company_summary_api = re.sub(r'<Market>', company, company_summary_api)
        try:
            summary = requests.request("GET", company_summary_api, timeout=timeout_seconds)
        except Exception as err:
            exception = True
        if exception is True:
            return jsonify({'Message': 'Unable to retrive the data for give company'})
        response = Response(
                response=json.dumps(summary.json()),
                status=200,
                mimetype='application/json'
        )
        return response
    return jsonify({'Message': 'Invalid input, Please provide the valid input'})
