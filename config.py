"""
Flask Application Configuration File

This module contains configuration settings for your Flask application.
These settings are typically used to configure database connections, secret keys,
debug mode, and other application-specific configurations.
"""

DEBUG = False
SECRET_KEY = ('Hs9>`nDZs]0zfQC'
              '+1s6#{oTDXg:VN"')
SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
PARENT_API = 'https://bittrex.github.io/api/v3#tag-Markets'
OVERALL_SUMMARY_API = 'https://api.bittrex.com/v3/markets/summaries'
MARKET_SUMMARY_API = 'https://api.bittrex.com/v3/markets/<Market>/summary'
