# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE = 'mydatabase.db'
    STRIPE_API_KEY = 'sk_test_51P8z4XSElIyrQVH2QnPsaVc17uN7hmMzTDzQd7VA7ij7ROAVsyFXAum3IrxrvD27l6G3ThvPjTD7ugicTtvZ2KIM00UNGZAKzT'
