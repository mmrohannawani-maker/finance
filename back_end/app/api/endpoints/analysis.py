from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.analysis_schema import Analysis, AnalysisCreate
from app.services.analysis_service import AnalysisService

router = APIRouter()

@router.post("/", response_model=Analysis)
def create_new_analysis(
    analysis: AnalysisCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start a new analysis"""
    service = AnalysisService(db)
    return service.start_analysis(analysis.file_id, analysis.analysis_type)

@router.get("/{analysis_id}", response_model=Analysis)
def get_analysis(analysis_id: str, db: Session = Depends(get_db)):
    """Get analysis by ID"""
    from app.crud.analysis_crud import get_analysis as crud_get_analysis
    analysis = crud_get_analysis(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

@router.get("/file/{file_id}", response_model=List[Analysis])
def get_file_analyses(file_id: str, db: Session = Depends(get_db)):
    """Get all analyses for a file"""
    from app.crud.analysis_crud import get_analyses_by_file
    return get_analyses_by_file(db, file_id)

@router.post("/run/summary/{file_id}", response_model=Analysis)
def run_summary_analysis(file_id: str, db: Session = Depends(get_db)):
    """Run summary statistics analysis"""
    service = AnalysisService(db)
    return service.start_analysis(file_id, "summary")

@router.post("/run/trend/{file_id}", response_model=Analysis)
def run_trend_analysis(file_id: str, db: Session = Depends(get_db)):
    """Run trend analysis"""
    service = AnalysisService(db)
    return service.start_analysis(file_id, "trend")

@router.post("/run/correlation/{file_id}", response_model=Analysis)
def run_correlation_analysis(file_id: str, db: Session = Depends(get_db)):
    """Run correlation analysis"""
    service = AnalysisService(db)
    return service.start_analysis(file_id, "correlation")