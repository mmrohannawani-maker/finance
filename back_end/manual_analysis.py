# manual_analysis_test.py
import sys
sys.path.append('.')
from app.database import SessionLocal
from app.services.analysis_service import AnalysisService
import pandas as pd

db = SessionLocal()
service = AnalysisService(db)

# Load data
from app.crud.file_data_crud import get_file_data
file_id = "cb791f6a-e759-4025-928e-885dee0693e1"
file_data = get_file_data(db, file_id, limit=100)
df = service._convert_filedata_to_dataframe(file_data)

print(f"DataFrame: {df.shape}")
print(f"Column dtypes:\n{df.dtypes}")

# Test summary statistics
print("\n=== TESTING SUMMARY STATISTICS ===")
results = service.summary_statistics(df)
print(f"Results generated for {len(results.get('columns', []))} columns")

# Check first column
if results.get('columns'):
    first_col = results['columns'][0]
    print(f"\nFirst column stats:")
    for key, value in first_col.items():
        print(f"  {key}: {value}")