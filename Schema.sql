-- File: schema.sql
-- This shows the structure of your database

-- Create database (you already did this)
CREATE DATABASE bank_reviews;

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

-- Create indexes for faster queries
CREATE INDEX idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX idx_reviews_sentiment ON reviews(sentiment);