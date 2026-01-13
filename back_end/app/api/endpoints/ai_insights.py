from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from app.services.openrouter_service import OpenRouterService
from app.services.file_service import FileService
from app.config import settings

router = APIRouter(prefix="/ai", tags=["ai-insights"])

openrouter_service = OpenRouterService()
file_service = FileService(settings.UPLOAD_DIR)

@router.post("/analyze-custom")
async def analyze_custom_data(
    data: list,
    query: str,
    db: AsyncSession = Depends(get_async_db)
):
    """Analyze custom data with AI"""
    try:
        if not data:
            raise HTTPException(status_code=400, detail="No data provided")
        
        analysis = await openrouter_service.analyze_data(data, query)
        
        return {
            "analysis": analysis,
            "data_points": len(data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize")
async def summarize_data(
    file_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """Generate summary of file data"""
    try:
        # Get file data
        result = await file_service.get_file_data(db, file_id, skip=0, limit=50)
        data = result["data"]
        
        if not data:
            raise HTTPException(status_code=400, detail="No data available")
        
        summary_prompt = """
        Provide a concise summary of this data including:
        1. Data structure (columns, data types)
        2. Key observations from the first 50 rows
        3. Potential use cases for this data
        4. Data quality assessment
        """
        
        summary = await openrouter_service.analyze_data(data, summary_prompt)
        
        return {
            "file_id": file_id,
            "summary": summary,
            "rows_summarized": len(data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
