# check_tables.py
import sys
import os
sys.path.append(os.path.dirname(__file__))

print("🔍 Checking database tables...")

try:
    from app.database import engine
    
    # Method 1: Using SQLAlchemy inspection
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print("\n📊 Tables in database:")
    for table in tables:
        print(f"  - {table}")
    
    if 'file_data' in tables:
        print("\n✅ SUCCESS: file_data table exists!")
        
        # Show columns
        print("\n📋 Columns in file_data table:")
        columns = inspector.get_columns('file_data')
        for col in columns:
            print(f"  - {col['name']}: {col['type']}")
    else:
        print("\n❌ file_data table does NOT exist!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()