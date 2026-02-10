# test_filedata.py
import sys
sys.path.append('.')
from app.database import SessionLocal
from app.crud.file_data_crud import get_file_data

db = SessionLocal()
file_id = "cb791f6a-e759-4025-928e-885dee0693e1"

# Get sample data
file_data = get_file_data(db, file_id, limit=5)
print(f"Got {len(file_data)} records")

if file_data:
    sample = file_data[0]
    print(f"\nSample object type: {type(sample)}")
    print(f"Sample object: {sample}")
    print(f"\nAll attributes:")
    for attr in dir(sample):
        if not attr.startswith('_'):
            print(f"  {attr}: {getattr(sample, attr, 'N/A')}")