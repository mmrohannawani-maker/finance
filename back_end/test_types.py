# test_types.py
import sys
import os
sys.path.append(os.path.dirname(__file__))

print("🔍 Checking type mismatches...")

try:
    from app.database import engine
    from sqlalchemy import text
    
    with engine.connect() as conn:
        print("1. Database column types:")
        result = conn.execute(text("""
            SELECT 
                column_name,
                data_type,
                udt_name
            FROM information_schema.columns 
            WHERE table_name = 'file_data'
            ORDER BY ordinal_position;
        """))
        
        for col, dtype, udt in result:
            print(f"   {col}: {dtype} ({udt})")
            
        print("\n2. Files table column types (for reference):")
        result = conn.execute(text("""
            SELECT 
                column_name,
                data_type,
                udt_name
            FROM information_schema.columns 
            WHERE table_name = 'files'
            ORDER BY ordinal_position;
        """))
        
        for col, dtype, udt in result:
            print(f"   {col}: {dtype} ({udt})")
            
except Exception as e:
    print(f"❌ Error: {e}")