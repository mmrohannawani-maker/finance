# test_trend_analysis.py
import sys
sys.path.append('.')
from app.database import SessionLocal
from app.services.analysis_service import AnalysisService
import pandas as pd

print("=== TESTING TREND ANALYSIS ===")
print()

db = SessionLocal()
service = AnalysisService(db)

# Load data
from app.crud.file_data_crud import get_file_data
file_id = "cb791f6a-e759-4025-928e-885dee0693e1"
file_data = get_file_data(db, file_id, limit=100)
df = service._convert_filedata_to_dataframe(file_data)

print(f"DataFrame shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print()

# Check for date columns
date_columns = []
for col in df.columns:
    try:
        pd.to_datetime(df[col], errors='raise')
        date_columns.append(col)
        print(f"✅ Found date column: {col}")
    except:
        pass

print(f"\nFound {len(date_columns)} date columns: {date_columns}")

# Check for numeric columns
numeric_columns = df.select_dtypes(include=[int, float]).columns.tolist()
print(f"Found {len(numeric_columns)} numeric columns: {numeric_columns}")

if date_columns and numeric_columns:
    print("\n=== RUNNING TREND ANALYSIS ===")
    results = service.trend_analysis(df)
    
    if "error" in results:
        print(f"❌ Error: {results['error']}")
    elif "trends" in results:
        print(f"✅ Generated {len(results['trends'])} trends:")
        for i, trend in enumerate(results['trends']):
            print(f"\nTrend {i+1}:")
            print(f"  Date column: {trend.get('date_column')}")
            print(f"  Value column: {trend.get('value_column')}")
            print(f"  Slope: {trend.get('slope')} (type: {type(trend.get('slope'))})")
            print(f"  Trend: {trend.get('trend')}")
            print(f"  Data points: {trend.get('data_points')} (type: {type(trend.get('data_points'))})")
        
        # Test JSON serialization
        import json
        try:
            json_str = json.dumps(results)
            print(f"\n✅ Trend results are JSON serializable!")
        except TypeError as e:
            print(f"\n❌ JSON serialization failed: {e}")
else:
    print("\n❌ Need at least 1 date column and 1 numeric column for trend analysis")

db.close()
print("\n=== TEST COMPLETE ===")