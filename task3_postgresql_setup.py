import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from datetime import datetime

def setup_postgresql(password="1234"):
    print("=" * 70)
    print("TASK 3: POSTGRESQL DATABASE FOR BANK REVIEWS")
    print("=" * 70)
    
    # Get password
    if password == "admin123":
        password = input("Enter your PostgreSQL password (default: admin123): ") or "admin123"
    
    # STEP 1: Create database tables
    print("\n📊 STEP 1: Creating database tables...")
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            database="bank_reviews",
            user="postgres",
            password=password
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Create tables based on YOUR CSV structure
        create_tables = """
        -- Drop tables if they exist
        DROP TABLE IF EXISTS reviews;
        DROP TABLE IF EXISTS banks;
        
        -- Create banks table
        CREATE TABLE banks (
            id SERIAL PRIMARY KEY,
            bank_code VARCHAR(50) UNIQUE NOT NULL,
            bank_name VARCHAR(100) NOT NULL,
            source VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create reviews table
        CREATE TABLE reviews (
            id SERIAL PRIMARY KEY,
            review_id VARCHAR(100) UNIQUE,
            bank_id INTEGER REFERENCES banks(id),
            review_text TEXT NOT NULL,
            rating INTEGER CHECK (rating >= 1 AND rating <= 5),
            review_date DATE,
            review_year INTEGER,
            review_month INTEGER,
            user_name VARCHAR(100),
            thumbs_up INTEGER DEFAULT 0,
            text_length INTEGER,
            source VARCHAR(50),
            sentiment VARCHAR(20),
            sentiment_score FLOAT,
            themes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create indexes for better performance
        CREATE INDEX idx_reviews_bank_id ON reviews(bank_id);
        CREATE INDEX idx_reviews_sentiment ON reviews(sentiment);
        CREATE INDEX idx_reviews_rating ON reviews(rating);
        CREATE INDEX idx_reviews_date ON reviews(review_date);
        """
        
        cur.execute(create_tables)
        print("✅ Tables created: 'banks' and 'reviews'")
        print("   • Added indexes for better query performance")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return
    
    # STEP 2: Look for data files
    print("\n📁 STEP 2: Looking for your data files...")
    
    csv_path = "data/processed/reviews_with_sentiment.csv"
    
    if os.path.exists(csv_path):
        # Load the data
        df = pd.read_csv(csv_path)
        print(f"✅ Found data: {csv_path}")
        print(f"   • Rows: {len(df)}")
        print(f"   • Columns: {df.columns.tolist()}")
        
        # Display sample
        print(f"\n📋 Sample data (first 3 rows):")
        print(df[['bank_name', 'rating', 'sentiment', 'review_text']].head(3).to_string())
        
        # STEP 3: Insert data
        print("\n💾 STEP 3: Inserting data into PostgreSQL...")
        
        try:
            # Reconnect
            conn = psycopg2.connect(
                host="localhost",
                database="bank_reviews",
                user="postgres",
                password=password
            )
            conn.autocommit = True
            cur = conn.cursor()
            
            # Insert banks
            print("   • Inserting banks...")
            # Get unique banks from your CSV
            bank_data = df[['bank_code', 'bank_name', 'source']].drop_duplicates()
            
            for _, row in bank_data.iterrows():
                cur.execute("""
                    INSERT INTO banks (bank_code, bank_name, source)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (bank_code) DO NOTHING;
                """, (row['bank_code'], row['bank_name'], row['source']))
            
            print(f"      Inserted {len(bank_data)} unique banks")
            
            # Get bank IDs for mapping
            cur.execute("SELECT bank_code, id FROM banks;")
            bank_map = {row[0]: row[1] for row in cur.fetchall()}
            
            # Insert reviews
            print("   • Inserting reviews...")
            inserted_count = 0
            error_count = 0
            
            for idx, row in df.iterrows():
                try:
                    # Convert date if needed
                    review_date = pd.to_datetime(row['review_date']).date() if pd.notna(row['review_date']) else None
                    
                    cur.execute("""
                        INSERT INTO reviews (
                            review_id, bank_id, review_text, rating, review_date,
                            review_year, review_month, user_name, thumbs_up,
                            text_length, source, sentiment, sentiment_score, themes
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (review_id) DO NOTHING;
                    """, (
                        row['review_id'], 
                        bank_map[row['bank_code']], 
                        str(row['review_text'])[:10000],  # Limit text length
                        int(row['rating']) if pd.notna(row['rating']) else None,
                        review_date,
                        int(row['review_year']) if pd.notna(row['review_year']) else None,
                        int(row['review_month']) if pd.notna(row['review_month']) else None,
                        str(row['user_name'])[:100] if pd.notna(row['user_name']) else None,
                        int(row['thumbs_up']) if pd.notna(row['thumbs_up']) else 0,
                        int(row['text_length']) if pd.notna(row['text_length']) else None,
                        str(row['source'])[:50] if pd.notna(row['source']) else None,
                        str(row['sentiment'])[:20] if pd.notna(row['sentiment']) else None,
                        float(row['sentiment_score']) if pd.notna(row['sentiment_score']) else None,
                        str(row['themes'])[:1000] if pd.notna(row['themes']) else None
                    ))
                    inserted_count += 1
                    
                    # Show progress every 100 rows
                    if (idx + 1) % 100 == 0:
                        print(f"      Processed {idx + 1}/{len(df)} rows...")
                        
                except Exception as e:
                    error_count += 1
                    if error_count <= 3:  # Show first 3 errors
                        print(f"      Warning: Error on row {idx}: {str(e)[:100]}")
                    continue
            
            print(f"      Successfully inserted {inserted_count} reviews")
            if error_count > 0:
                print(f"      Skipped {error_count} rows with errors")
            
            # Verify the data
            print("\n✅ STEP 4: Verifying database...")
            cur.execute("SELECT COUNT(*) FROM banks;")
            bank_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM reviews;")
            review_count = cur.fetchone()[0]
            
            print(f"   • Banks in database: {bank_count}")
            print(f"   • Reviews in database: {review_count}")
            
            # Show some statistics
            cur.execute("""
                SELECT 
                    b.bank_name,
                    COUNT(r.id) as review_count,
                    ROUND(AVG(r.rating), 2) as avg_rating,
                    COUNT(CASE WHEN r.sentiment = 'POSITIVE' THEN 1 END) as positive_reviews,
                    COUNT(CASE WHEN r.sentiment = 'NEGATIVE' THEN 1 END) as negative_reviews
                FROM banks b
                LEFT JOIN reviews r ON b.id = r.bank_id
                GROUP BY b.id, b.bank_name
                ORDER BY review_count DESC;
            """)
            
            stats = cur.fetchall()
            print(f"\n📈 Bank Review Statistics:")
            for stat in stats[:5]:  # Show top 5
                print(f"   • {stat[0]}: {stat[1]} reviews, Avg rating: {stat[2]}")
            
            cur.close()
            conn.close()
            
            print("\n" + "=" * 70)
            print("✅ DATABASE SETUP COMPLETE!")
            print("=" * 70)
            print("\nYou can now connect with:")
            print(f"   Database: bank_reviews")
            print(f"   Username: postgres")
            print(f"   Host: localhost")
            print(f"   Tables: banks, reviews")
            
        except Exception as e:
            print(f"❌ Error inserting data: {e}")
            
    else:
        print(f"❌ Data file not found: {csv_path}")
        print("Please make sure your CSV file exists at the specified path.")

if __name__ == "__main__":
    setup_postgresql("1234")  # Or use your actual password