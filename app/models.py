"""
User Models for Your Flask Application

This module defines the SQLAlchemy User model for your Flask application.
The User model represents user data in the database.

Classes:
    User: Represents a user in the application.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
        The User model represents user data in the database.
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(300), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    @property
    def is_active(self):
        return self.id
