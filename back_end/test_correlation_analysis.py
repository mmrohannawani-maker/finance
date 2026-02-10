# test_correlation_analysis.py
import sys
sys.path.append('.')
from app.database import SessionLocal
from app.services.analysis_service import AnalysisService
import pandas as pd

print("=== TESTING CORRELATION ANALYSIS ===")
print()

db = SessionLocal()
service = AnalysisService(db)

# Load data
from app.crud.file_data_crud import get_file_data
file_id = "cb791f6a-e759-4025-928e-885dee0693e1"
file_data = get_file_data(db, file_id, limit=100)
df = service._convert_filedata_to_dataframe(file_data)

print(f"DataFrame shape: {df.shape}")
print()

# Check numeric columns
numeric_df = df.select_dtypes(include=[int, float])
print(f"Numeric columns found: {list(numeric_df.columns)}")
print(f"Numeric DataFrame shape: {numeric_df.shape}")

if numeric_df.shape[1] >= 2:
    print("\n=== RUNNING CORRELATION ANALYSIS ===")
    results = service.correlation_analysis(df)
    
    if "error" in results:
        print(f"❌ Error: {results['error']}")
    elif "correlations" in results:
        print(f"✅ Generated {len(results['correlations'])} correlations:")
        
        # Show top 5 correlations
        for i, corr in enumerate(results['correlations'][:5]):
            print(f"\nCorrelation {i+1}:")
            print(f"  Columns: {corr.get('column_a')} ↔ {corr.get('column_b')}")
            print(f"  Correlation: {corr.get('correlation')} (type: {type(corr.get('correlation'))})")
            print(f"  Strength: {corr.get('strength')}")
            print(f"  Interpretation: {corr.get('interpretation')}")
        
        # Test JSON serialization
        import json
        try:
            json_str = json.dumps(results)
            print(f"\n✅ Correlation results are JSON serializable!")
            print(f"  JSON length: {len(json_str)} characters")
        except TypeError as e:
            print(f"\n❌ JSON serialization failed: {e}")
else:
    print("❌ Need at least 2 numeric columns for correlation analysis")

db.close()
print("\n=== TEST COMPLETE ===")