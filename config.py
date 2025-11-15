import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    TOKEN = ""
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")