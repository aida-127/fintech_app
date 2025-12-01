"""
Configuration file for Bank Reviews Analysis Project
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env in same folder
load_dotenv()

# Google Play Store App IDs
APP_IDS = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'Dashen Bank': 'com.dashen.dashensuperapp'
}

# Bank Names Mapping
BANK_NAMES = {
    'CBE': 'Commercial Bank of Ethiopia',
    'BOA': 'Bank of Abyssinia',
    'Dashen Bank': 'Dashen Bank'
}

# Scraping Configuration
SCRAPING_CONFIG = {
    'reviews_per_bank': 400,
    'max_retries': 3,
    'lang': 'en',
    'country': 'et'  # Ethiopia
}

# File Paths - Use relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATHS = {
    'raw': os.path.join(BASE_DIR, 'data', 'raw'),
    'processed': os.path.join(BASE_DIR, 'data', 'processed'),
    'raw_reviews': os.path.join(BASE_DIR, 'data', 'raw', 'reviews_raw.csv'),
    'processed_reviews': os.path.join(BASE_DIR, 'data', 'processed', 'reviews_processed.csv'),
    'sentiment_results': os.path.join(BASE_DIR, 'data', 'processed', 'reviews_with_sentiment.csv'),
    'final_results': os.path.join(BASE_DIR, 'data', 'processed', 'reviews_final.csv')
}

# Create directories if they don't exist
os.makedirs(DATA_PATHS['raw'], exist_ok=True)
os.makedirs(DATA_PATHS['processed'], exist_ok=True)