# thematic_analysis.py
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

# Load data
df = pd.read_csv('data/processed/reviews_with_sentiment.csv')

# Load spaCy
nlp = spacy.load("en_core_web_sm")

# Define banking themes with keywords
THEMES = {
    'Login & Access': ['login', 'password', 'fingerprint', 'access', 'authenticate'],
    'Transactions': ['transfer', 'payment', 'send money', 'transaction', 'fee'],
    'App Performance': ['slow', 'crash', 'lag', 'freeze', 'loading', 'bug'],
    'User Interface': ['interface', 'design', 'layout', 'button', 'menu', 'navigation'],
    'Customer Support': ['support', 'help', 'service', 'contact', 'response'],
    'Security': ['security', 'safe', 'hack', 'privacy', 'fraud']
}

def extract_themes(text):
    """Assign themes based on keywords"""
    text_lower = str(text).lower()
    found = []
    for theme, keywords in THEMES.items():
        for keyword in keywords:
            if keyword in text_lower:
                found.append(theme)
                break  # Found one keyword, move to next theme
    return ', '.join(found) if found else 'General Feedback'

# Add themes to dataframe
df['themes'] = df['review_text'].apply(extract_themes)

# Save with themes
df.to_csv('data/processed/reviews_with_sentiment_themes.csv', index=False)
print(f"✅ Themes added to {len(df)} reviews")

# Generate theme report
print("\n📊 THEMES BY BANK:")
for bank in df['bank_name'].unique():
    bank_df = df[df['bank_name'] == bank]
    
    # Count themes
    theme_counter = Counter()
    for themes in bank_df['themes']:
        for theme in themes.split(', '):
            if theme != 'General Feedback':
                theme_counter[theme] += 1
    
    print(f"\n{bank} (Top 3 themes):")
    for theme, count in theme_counter.most_common(3):
        pct = count / len(bank_df) * 100
        print(f"  {theme}: {count} mentions ({pct:.1f}%)")
        
        # Show example
        example = bank_df[bank_df['themes'].str.contains(theme)].iloc[0]['review_text'][:100]
        print(f"    Example: '{example}...'")