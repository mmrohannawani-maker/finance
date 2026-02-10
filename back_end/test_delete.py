# test_delete_fixed.py
import sys
import os
sys.path.append(os.path.dirname(__file__))

print("🧪 Testing delete with fixed model...")

try:
    from app.database import SessionLocal
    from app.models import FileData
    from sqlalchemy import select
    
    db = SessionLocal()
    
    # Get a file_id that has data
    result = db.execute(select(FileData).limit(1))
    file_data = result.scalar_one_or_none()
    
    if file_data:
        file_id = file_data.file_id
        print(f"Testing delete for file_id: {file_id}")
        
        # Check model column names
        print(f"\n📋 FileData model columns:")
        for col in FileData.__table__.columns:
            print(f"  - {col.name}: {col.type}")
        
        # Count before
        count_before = db.query(FileData).filter(FileData.file_id == file_id).count()
        print(f"\n📊 Rows before delete: {count_before}")
        
        if count_before > 0:
            # Try delete
            from app.crud.file_data_crud import delete_file_data
            
            print("🗑️ Calling delete_file_data()...")
            try:
                delete_file_data(db, str(file_id))
                print("✅ delete_file_data() completed")
                
                # Count after
                count_after = db.query(FileData).filter(FileData.file_id == file_id).count()
                print(f"📊 Rows after delete: {count_after}")
                
                if count_after == 0:
                    print("🎉 DELETE SUCCESSFUL!")
                else:
                    print("❌ Delete failed - rows still exist")
                    
            except Exception as e:
                print(f"❌ Error in delete_file_data: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("⚠️ No data to delete")
    else:
        print("❌ No file_data records found")
        
except Exception as e:
    print(f"❌ Overall error: {e}")
    import traceback
    traceback.print_exc()