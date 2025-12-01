"""
Task 2: Sentiment and Thematic Analysis
"""
import pandas as pd
import numpy as np
from transformers import pipeline
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import re

# Load cleaned data
df = pd.read_csv('data/processed/reviews_processed.csv')
print(f"Loaded {len(df)} reviews")

# 1. SENTIMENT ANALYSIS
print("\n=== Sentiment Analysis ===")
sentiment_analyzer = pipeline("sentiment-analysis", 
                             model="distilbert-base-uncased-finetuned-sst-2-english")

def get_sentiment(text):
    """Get sentiment for single review"""
    try:
        result = sentiment_analyzer(text[:512])[0]  # Limit text length
        return result['label'], round(result['score'], 3)
    except:
        return 'NEUTRAL', 0.5

# Apply to all reviews
df[['sentiment', 'sentiment_score']] = df['review_text'].apply(
    lambda x: pd.Series(get_sentiment(x))
)

# 2. THEMATIC ANALYSIS
print("\n=== Thematic Analysis ===")
nlp = spacy.load("en_core_web_sm")

# Define banking themes
BANKING_THEMES = {
    'Login & Security': ['login', 'password', 'fingerprint', 'security', 'authenticate'],
    'Transactions': ['transfer', 'payment', 'send', 'receive', 'transaction', 'money'],
    'App Performance': ['slow', 'crash', 'lag', 'freeze', 'loading', 'bug'],
    'User Interface': ['interface', 'design', 'layout', 'button', 'menu', 'navigation'],
    'Customer Service': ['support', 'help', 'service', 'contact', 'response', 'call']
}

def assign_theme(text):
    """Assign review to themes based on keywords"""
    text_lower = text.lower()
    themes_found = []
    for theme, keywords in BANKING_THEMES.items():
        if any(keyword in text_lower for keyword in keywords):
            themes_found.append(theme)
    return ', '.join(themes_found) if themes_found else 'Other'

# Assign themes
df['themes'] = df['review_text'].apply(assign_theme)

# 3. SAVE RESULTS
output_path = 'data/processed/reviews_with_sentiment.csv'
df.to_csv(output_path, index=False)
print(f"\n✅ Saved results to: {output_path}")
print(f"   Sentiment analyzed: {len(df)} reviews ({len(df)/1200*100:.1f}%)")

# 4. SUMMARY STATS
print("\n=== Summary ===")
for bank in df['bank_name'].unique():
    bank_df = df[df['bank_name'] == bank]
    pos = (bank_df['sentiment'] == 'POSITIVE').mean() * 100
    print(f"{bank}: {pos:.1f}% positive, {len(bank_df)} reviews")