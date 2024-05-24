# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE = 'mydatabase.db'
    STRIPE_API_KEY = ' Below is a stipe_API key'
# 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