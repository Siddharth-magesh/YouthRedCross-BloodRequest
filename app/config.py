import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_MAPS_API = os.getenv('GOOGLE_MAPS_API')
    BASE_MAPS_URL = os.getenv('BASE_MAPS_URL')