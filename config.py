import os
from dotenv import load_dotenv
from pathlib import Path

# Force load .env from project root
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/uploads')

print("DB URL:", os.getenv('DATABASE_URL'))  # debug
