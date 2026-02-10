# create_analysis_table.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.config import settings  # Import from settings, not database

# Create analysis table SQL
create_table_sql = """
CREATE TABLE IF NOT EXISTS analyses (
    id VARCHAR(255) PRIMARY KEY,
    file_id VARCHAR(255) NOT NULL,
    analysis_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    results JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);
"""

# Create indexes SQL
create_indexes_sql = """
CREATE INDEX IF NOT EXISTS idx_analyses_file_id ON analyses(file_id);
CREATE INDEX IF NOT EXISTS idx_analyses_status ON analyses(status);
CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON analyses(created_at);
"""

print(f"Using database: {settings.DATABASE_URL}")

# Execute
try:
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        # Create table
        conn.execute(text(create_table_sql))
        
        # Create indexes
        conn.execute(text(create_indexes_sql))
        
        conn.commit()
        print("✅ Analysis table created successfully!")
        print("✅ Indexes created successfully!")
        
except Exception as e:
    print(f"❌ Error: {e}")