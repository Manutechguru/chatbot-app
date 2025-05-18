import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # ✅ Load Gemini key