# test_csv_upload_fixed.py
import sys
import os
sys.path.append(os.path.dirname(__file__))

print("🧪 Testing CSV data storage (Fixed)...")

try:
    from app.database import engine
    from sqlalchemy import text
    
    with engine.connect() as conn:
        # Check row count in file_data table
        result = conn.execute(text("SELECT COUNT(*) FROM file_data"))
        row_count = result.scalar()
        
        print(f"\n📊 Current rows in file_data table: {row_count}")
        
        if row_count > 0:
            print("✅ Data is being saved to file_data table!")
            
            # First, check what the JSON data actually contains
            print("\n📝 Sample data (first 2 rows, full JSON):")
            result = conn.execute(text("""
                SELECT file_id, row_index, data
                FROM file_data 
                ORDER BY created_at 
                LIMIT 2;
            """))
            
            rows = result.fetchall()
            for row in rows:
                file_id, row_index, json_data = row
                print(f"\n  File: {file_id}, Row: {row_index}")
                
                if json_data:
                    # Try to show first few key-value pairs
                    try:
                        if isinstance(json_data, dict):
                            items = list(json_data.items())[:3]  # First 3 items
                            for key, value in items:
                                print(f"    {key}: {value}")
                        else:
                            print(f"    JSON data: {str(json_data)[:100]}...")
                    except:
                        print(f"    Raw data: {str(json_data)[:100]}...")
                else:
                    print("    ⚠️ JSON data is NULL/empty")
            
            # Count files with data
            print("\n📁 Files with stored data:")
            result = conn.execute(text("""
                SELECT 
                    f.filename, 
                    COUNT(fd.id) as row_count,
                    MIN(fd.created_at) as first_saved,
                    MAX(fd.created_at) as last_saved
                FROM files f
                LEFT JOIN file_data fd ON f.id::text = fd.file_id::text
                GROUP BY f.id, f.filename
                HAVING COUNT(fd.id) > 0
                ORDER BY row_count DESC;
            """))
            
            files_with_data = 0
            for filename, count, first, last in result:
                print(f"  - {filename}: {count} rows (saved: {first})")
                files_with_data += 1
            
            if files_with_data == 0:
                print("  ⚠️ No files have data in file_data table")
                
            # Check if data column has actual values
            print("\n🔍 Data column analysis:")
            result = conn.execute(text("""
                SELECT 
                    COUNT(*) as total_rows,
                    COUNT(data) as rows_with_data,
                    COUNT(CASE WHEN data IS NULL THEN 1 END) as null_rows,
                    COUNT(CASE WHEN data::text = '{}' THEN 1 END) as empty_json_rows
                FROM file_data;
            """))
            
            total, with_data, null_rows, empty_json = result.fetchone()
            print(f"  Total rows: {total}")
            print(f"  Rows with data: {with_data}")
            print(f"  NULL rows: {null_rows}")
            print(f"  Empty JSON rows: {empty_json}")
            
        else:
            print("❌ file_data table is EMPTY!")
            print("\n⚠️  Next steps:")
            print("   1. Upload a CSV file through your frontend")
            print("   2. Check console logs for errors")
            print("   3. Make sure save_csv_data() is being called")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()