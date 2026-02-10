# test_file_upload.py
import sys
sys.path.append('.')
from app.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

# Check all tables
print("=== DATABASE CHECK ===")
tables = db.execute(text("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
""")).fetchall()

print("Tables:", [t[0] for t in tables])

# Check files table
try:
    files = db.execute(text("SELECT id, filename, created_at FROM files")).fetchall()
    print(f"\nFiles table has {len(files)} rows:")
    for f in files[:5]:
        print(f"  ID: {f[0]}, Name: {f[1]}, Created: {f[2]}")
except:
    print("\nFiles table doesn't exist or has no data")

# Check file_data table
try:
    file_data_count = db.execute(text("SELECT COUNT(*) FROM file_data")).scalar()
    print(f"\nFile_data table has {file_data_count} rows total")
except:
    print("\nFile_data table doesn't exist")