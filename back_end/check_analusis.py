# check_analyses.py
import sys
sys.path.append('.')
from app.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

print("=== CHECKING ANALYSES TABLE ===")
print()

# Query 1: Get all analyses
try:
    result = db.execute(text("""
        SELECT 
            id, 
            file_id, 
            analysis_type, 
            status,
            completed_at,
            (results IS NOT NULL) as has_results,
            created_at
        FROM analyses 
        ORDER BY created_at DESC 
        LIMIT 10
    """))
    
    analyses = result.fetchall()
    print(f"Found {len(analyses)} analyses in database:")
    print("-" * 80)
    
    for i, row in enumerate(analyses):
        print(f"{i+1}. ID: {row[0]}")
        print(f"   File ID: {row[1]} (type: {type(row[1])})")
        print(f"   Type: {row[2]}, Status: {row[3]}")
        print(f"   Completed: {row[4]}, Has Results: {row[5]}")
        print(f"   Created: {row[6]}")
        print()
        
except Exception as e:
    print(f"Error querying analyses: {e}")

print("=" * 80)
print()

# Query 2: Check for your specific file
print("=== CHECKING FOR YOUR FILE ===")
file_id_str = "cb791f6a-e759-4025-928e-885dee0693e1"

try:
    # Try as string first
    result = db.execute(text("""
        SELECT id, file_id, analysis_type, status, completed_at
        FROM analyses 
        WHERE file_id = :file_id
    """), {"file_id": file_id_str})
    
    rows = result.fetchall()
    print(f"\nSearching as STRING '{file_id_str}':")
    print(f"Found {len(rows)} analyses")
    
    for row in rows:
        print(f"  - ID: {row[0]}, Type: {row[2]}, Status: {row[3]}, Completed: {row[4]}")
    
except Exception as e:
    print(f"String search error: {e}")

print()
print("=" * 80)
print()

# Query 3: Check file_data table for comparison
print("=== CHECKING FILE_DATA TABLE ===")
try:
    result = db.execute(text("""
        SELECT DISTINCT file_id 
        FROM file_data 
        LIMIT 5
    """))
    
    file_ids = result.fetchall()
    print(f"\nFile IDs in file_data table:")
    for fid in file_ids:
        print(f"  - {fid[0]} (type: {type(fid[0])})")
        
except Exception as e:
    print(f"Error checking file_data: {e}")

db.close()
print("\n=== DONE ===")