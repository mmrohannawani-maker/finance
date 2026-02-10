# test_analysis.py
import sys
sys.path.append('.')
from app.database import SessionLocal
from app.services.analysis_service import AnalysisService
from app.crud.analysis_crud import create_analysis
from app.schemas.analysis_schema import AnalysisCreate
import asyncio

db = SessionLocal()
file_id = "cb791f6a-e759-4025-928e-885dee0693e1"

# Create an analysis record
analysis_create = AnalysisCreate(
    file_id=file_id,
    analysis_type="summary",
    status="running"
)

from app.crud.analysis_crud import create_analysis
analysis = create_analysis(db, analysis_create)
print(f"Created analysis: {analysis.id}")

# Run the analysis
service = AnalysisService(db)
asyncio.run(service.run_analysis(analysis.id, file_id, "summary"))

# Check result
from app.crud.analysis_crud import get_analysis
result = get_analysis(db, analysis.id)
print(f"\nAnalysis result - Status: {result.status}")
if result.results:
    print(f"Has results: Yes, {len(result.results.get('columns', []))} columns analyzed")
else:
    print(f"Has results: No")