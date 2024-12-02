import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_MAPS_API = os.getenv("GOOGLE_MAPS_API")
    BASE_MAPS_URL = os.getenv("BASE_MAPS_URL")
    BASE_MAIL_ADDRESS = os.getenv("BASE_MAIL_ADDRESS")
    
    # Email configurations
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS") == 'True'
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL") == 'True'

    CAPTCHA_ENABLE = True
    CAPTCHA_LENGTH = 5
    CAPTCHA_WIDTH = 150
    CAPTCHA_HEIGHT = 60
    CAPTCHA_LOG = True
    CAPTCHA_INCLUDE_ALPHABET = False
    CAPTCHA_INCLUDE_NUMERIC = True
    CAPTCHA_INCLUDE_PUNCTUATION = False 

    SESSION_TYPE = 'filesystem'
    APSCHEDULER_TIMEZONE = 'Asia/Kolkata'
