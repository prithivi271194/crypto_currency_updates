## Project Overview
This is a Flask-based web application that will extarct the overall crypto currency market summary.

## Table of Contents
- [Features]
- [Requirements]
- [Setup]
- [Usage]

## Features
- User Registration: Users can sign up for the application by providing a unique username and a secure password. 
- User Login: Registered users can log in using their credentials. The system checks the provided username and password against the stored data for authentication.
- Token Management : When a user logs in or is authenticated, It will create a JWT containing user-specific data (claims), such as username and password. This token is signed with a secret key.
- Token Expiration: Once the token is created the authencation will expire after 30mins, the user must re-authenticate.
- Access Control: Certain routes and resources are protected and require authentication. Unauthorized users are redirected to the login page. 

## Requirements
List the software and dependencies required to run the project. Include links or version information if applicable.

- [Python](https://www.python.org/) (>= 3.9)
- [Flask](https://flask.palletsprojects.com/) (>= 2.3.3)
- Other Python package dependencies are added in the requirements.txt file.

## Setup
Provide instructions for setting up and configuring the project locally. Include steps for installing dependencies and any configuration steps.

```bash
# Clone the repository
git clone [repository_url]

# Change into the project directory
cd [project_directory]

# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment (Windows)
venv\Scripts\activate

# Activate the virtual environment (Linux/macOS)
source venv/bin/activate

# Install project dependencies
pip install -r requirements.txt

# Set environment variables if needed
export FLASK_ENV=development

# Initialize the database (if applicable)
flask db init
flask db upgrade

# Run the application
python run.py

```
## Usage
Run the main script run.py to start the application. Please replace the hostname with your local/public ip address.

1. http://hostname:5000/apidocs/ - open the Swagger api dcoumentation.
2. http://hostname:5000/v1/public/register - To register a new user
3. http://hostname:5000/v1/public/login - To login with the user credentials
4. http://hostname:5000/v1/private/logout - To logout the current user from the application
5. http://hostname:5000/v1/private/summary - To get the overall Market summary
6. http://hostname:5000/v1/private/<market>/summary - To get the particular market summary

