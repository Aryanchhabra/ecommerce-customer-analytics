"""
Database module for storing predictions and analytics results
"""

import sqlite3
import pandas as pd
from datetime import datetime
from typing import Optional, List, Dict

class AnalyticsDB:
    def __init__(self, db_path='analytics.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                prediction_type TEXT,
                prediction_value REAL,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Customer segments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_segments (
                customer_id INTEGER PRIMARY KEY,
                segment TEXT,
                recency REAL,
                frequency REAL,
                monetary REAL,
                rfm_score INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Analytics cache table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics_cache (
                cache_key TEXT PRIMARY KEY,
                cache_value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_prediction(self, customer_id: int, prediction_type: str, 
                       prediction_value: float, confidence: Optional[float] = None):
        """Save a prediction to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions (customer_id, prediction_type, prediction_value, confidence)
            VALUES (?, ?, ?, ?)
        ''', (customer_id, prediction_type, prediction_value, confidence))
        
        conn.commit()
        conn.close()
    
    def save_customer_segment(self, customer_id: int, segment: str, 
                             recency: float, frequency: float, 
                             monetary: float, rfm_score: int):
        """Save or update customer segment"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO customer_segments 
            (customer_id, segment, recency, frequency, monetary, rfm_score)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (customer_id, segment, recency, frequency, monetary, rfm_score))
        
        conn.commit()
        conn.close()
    
    def get_customer_history(self, customer_id: int) -> pd.DataFrame:
        """Get prediction history for a customer"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('''
            SELECT * FROM predictions 
            WHERE customer_id = ?
            ORDER BY created_at DESC
        ''', conn, params=(customer_id,))
        conn.close()
        return df
    
    def get_segment_stats(self) -> pd.DataFrame:
        """Get statistics by segment"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('''
            SELECT 
                segment,
                COUNT(*) as customer_count,
                AVG(monetary) as avg_monetary,
                AVG(frequency) as avg_frequency,
                AVG(recency) as avg_recency
            FROM customer_segments
            GROUP BY segment
        ''', conn)
        conn.close()
        return df

