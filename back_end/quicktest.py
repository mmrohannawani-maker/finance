# quick_test.py
import sys
sys.path.append('.')
from app.database import SessionLocal
from app.services.analysis_service import AnalysisService

db = SessionLocal()
service = AnalysisService(db)

# Test the conversion
file_id = "cb791f6a-e759-4025-928e-885dee0693e1"
from app.crud.file_data_crud import get_file_data

file_data = get_file_data(db, file_id, limit=5)
print(f"Got {len(file_data)} FileData records")

if file_data:
    df = service._convert_filedata_to_dataframe(file_data)
    print(f"DataFrame created: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"First row:\n{df.iloc[0]}")