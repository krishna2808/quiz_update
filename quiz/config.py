import os 
from dotenv import load_dotenv


class Config:
      # SECRET_KEY = 'im krishna'
      SECRET_KEY = os.environ.get('SECRET_KEY')
      SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
      # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:2222@localhost:5432/quiz"
      SQLALCHEMY_TRACK_MODIFICATIONS = False
      
      ADMIN_TOKEN = 'krishna'