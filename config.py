import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'  # Change this to a random string
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///blog.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # Use Config.SQLALCHEMY_DATABASE_URI to reference the parent class attribute
    if Config.SQLALCHEMY_DATABASE_URI and Config.SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)