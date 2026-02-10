#!/usr/bin/env python3
# create_tables.py
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL not found in .env file")
    print("Make sure your .env has: DATABASE_URL=postgresql://user:pass@localhost/dbname")
    exit(1)

print(f"🔗 Using database: {DATABASE_URL.split('@')[-1]}")

# SQL to create file_data table
sql_commands = """
-- Create file_data table
CREATE TABLE IF NOT EXISTS file_data (
    id SERIAL PRIMARY KEY,
    file_id VARCHAR(255) NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    row_index INTEGER NOT NULL,
    row_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_file_data_file_id ON file_data(file_id);

-- Verify the table was created
SELECT '✅ file_data table created successfully' as status;
"""

print("📦 Creating file_data table...")

try:
    # Run the SQL using psql command
    result = subprocess.run(
        ["psql", DATABASE_URL, "-c", sql_commands],
        capture_output=True,
        text=True,
        check=True
    )
    
    print("✅ Success!")
    print(result.stdout)
    
except subprocess.CalledProcessError as e:
    print(f"❌ Failed to create table:")
    print(f"Error: {e.stderr}")
except FileNotFoundError:
    print("❌ ERROR: 'psql' command not found!")
    print("Install PostgreSQL client or use direct SQLAlchemy method.")
    
    # Alternative: Use SQLAlchemy directly
    print("\n🔧 Trying SQLAlchemy method...")
    try:
        from app.database import engine
        from app.models.file_data_model import FileData
        from app.models.file_model import File
        
        # Import all models so SQLAlchemy knows about them
        import app.models
        
        # Create tables
        from sqlalchemy import text
        
        with engine.connect() as conn:
            # Create table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS file_data (
                    id SERIAL PRIMARY KEY,
                    file_id VARCHAR(255) NOT NULL,
                    row_index INTEGER NOT NULL,
                    row_data JSONB NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Add foreign key constraint
            conn.execute(text("""
                ALTER TABLE file_data 
                ADD CONSTRAINT fk_file_data_file 
                FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
            """))
            
            # Create index
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_file_data_file_id 
                ON file_data(file_id)
            """))
            
            conn.commit()
            print("✅ Successfully created file_data table using SQLAlchemy!")
            
    except Exception as e:
        print(f"❌ SQLAlchemy also failed: {e}")