# app/api/endpoints/reports.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os

# Use your existing imports
from app.database import get_db  
from app.crud.analysis_crud import get_analysis_by_file_and_type, get_latest_analysis
from app.services.report_service import ReportService
from app.schemas.analysis_schema import ReportRequest
import tempfile

router = APIRouter()
report_service = ReportService()

@router.post("/generate")
async def generate_report(request: ReportRequest, db: Session = Depends(get_db)):
    """Generate PDF report from existing analysis results"""
    print(f"[DEBUG] Generate report called: file_id={request.file_id}, type={request.analysis_type}")
    
    try:
        # 1. Get existing analysis results from database
        print(f"[DEBUG] Looking for existing analysis in database...")
        analysis = get_analysis_by_file_and_type(
            db, 
            file_id=request.file_id, 
            analysis_type=request.analysis_type,
            status="completed"  # Only get completed analyses
        )
        
        # If not found, get latest completed analysis
        if not analysis:
            print(f"[DEBUG] No specific analysis found, getting latest...")
            analysis = get_latest_analysis(
                db,
                file_id=request.file_id,
                status="completed"
            )
        
        if not analysis or not analysis.results:
            raise HTTPException(
                status_code=404, 
                detail=f"No completed {request.analysis_type} analysis found for this file. Run analysis first."
            )
        
        print(f"[DEBUG] Found analysis ID: {analysis.id} with results")
        
        # 2. Create PDF from results
        pdf_path = report_service.create_pdf_report(
            analysis_results=analysis.results,
            analysis_type=request.analysis_type
        )
        
        # 3. Return PDF
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"{request.analysis_type}_report_{request.file_id[:8]}.pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Report generation failed: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate report: {str(e)}"
        )