## 📊 Task 3: PostgreSQL Database Implementation

### **Database Details**
- **Database Name:** `bank_reviews`
- **Total Tables:** 2 (`banks` and `reviews`)
- **Total Data:** 3 banks, 1,200 customer reviews
- **Insertion Method:** Python script with psycopg2

### **Schema Structure**

#### **banks table**
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| bank_code | VARCHAR(50) | Unique bank identifier |
| bank_name | VARCHAR(100) | Bank name |
| source | VARCHAR(50) | Data source |
| created_at | TIMESTAMP | Creation timestamp |

#### **reviews table**
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| review_id | VARCHAR(100) | Unique review ID |
| bank_id | INTEGER | Foreign key to banks |
| review_text | TEXT | Review content |
| rating | INTEGER | Star rating (1-5) |
| review_date | DATE | Review date |
| sentiment | VARCHAR(20) | POSITIVE/NEGATIVE/NEUTRAL |
| sentiment_score | FLOAT | Sentiment score (0-1) |
| source | VARCHAR(50) | Review source |

### **Statistics Summary**
| Bank Name | Reviews | Avg Rating | Positive | Negative |
|-----------|---------|------------|----------|----------|
| Commercial Bank of Ethiopia | 400 | 4.13 | 257 | 143 |
| Dashen Bank | 400 | 3.96 | 256 | 144 |
| Bank of Abyssinia | 400 | 3.38 | 184 | 216 |

### **Files Included**
- `task3_postgresql_setup.py` - Database creation and data insertion
- `schema.sql` - SQL schema definition
- `verification_queries.sql` - Data validation queries

### **How to Run**
```bash
# 1. Ensure PostgreSQL is running
# 2. Execute the Python script
python task3_postgresql_setup.py
# 3. Enter PostgreSQL password when prompted