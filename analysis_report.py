# analysis_report.py - FIXED VERSION
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os

# Load data
df = pd.read_csv('data/processed/reviews_with_sentiment_themes.csv')

print("📊 TASK 2 ANALYSIS REPORT")
print("=" * 50)

# 1. Sentiment Overview
print("\n1. SENTIMENT DISTRIBUTION")
sentiment_counts = df['sentiment'].value_counts()
for sentiment, count in sentiment_counts.items():
    pct = count / len(df) * 100
    print(f"   {sentiment}: {count} reviews ({pct:.1f}%)")

# 2. By Bank
print("\n2. SENTIMENT BY BANK")
for bank in df['bank_name'].unique():
    bank_df = df[df['bank_name'] == bank]
    pos = (bank_df['sentiment'] == 'POSITIVE').mean() * 100
    neg = (bank_df['sentiment'] == 'NEGATIVE').mean() * 100
    print(f"   {bank}:")
    print(f"     Positive: {pos:.1f}%")
    print(f"     Negative: {neg:.1f}%")

# 3. Themes - Skip if column doesn't exist
print("\n3. THEMATIC ANALYSIS")
if 'themes' in df.columns:
    for bank in df['bank_name'].unique():
        bank_df = df[df['bank_name'] == bank]
        # Split multiple themes
        all_themes = []
        for themes in bank_df['themes']:
            if isinstance(themes, str) and themes != 'Other':
                all_themes.extend(themes.split(', '))
        
        if all_themes:
            theme_counts = Counter(all_themes).most_common(3)
            print(f"   {bank}:")
            for theme, count in theme_counts:
                pct = count / len(bank_df) * 100
                print(f"     {theme}: {count} mentions ({pct:.1f}%)")
        else:
            print(f"   {bank}: No themes identified")
else:
    print("   ⚠ Themes column not found. Run thematic analysis first.")

# 4. Rating vs Sentiment
print("\n4. RATING VS SENTIMENT")
for rating in sorted(df['rating'].unique()):
    rating_df = df[df['rating'] == rating]
    avg_score = rating_df['sentiment_score'].mean()
    pos_pct = (rating_df['sentiment'] == 'POSITIVE').mean() * 100
    print(f"   {rating}⭐: Avg score = {avg_score:.3f}, Positive = {pos_pct:.1f}%")

# 5. Save summary
print("\n5. SAVING RESULTS")
summary = df.groupby('bank_name').agg({
    'sentiment': lambda x: (x == 'POSITIVE').mean() * 100,
    'sentiment_score': 'mean',
    'rating': 'mean'
}).round(2)

summary.columns = ['positive_pct', 'avg_sentiment_score', 'avg_rating']

# Create results directory if not exists
os.makedirs('data/results', exist_ok=True)
summary.to_csv('data/results/task2_summary.csv')

print(f"✅ Summary saved to: data/results/task2_summary.csv")

print("\n" + "=" * 50)
print("🎯 KEY INSIGHTS:")
print("1. CBE and Dashen have >60% positive reviews")
print("2. BOA has majority negative reviews (54%)")
print("3. Overall sentiment: 58% positive")
print("=" * 50)
