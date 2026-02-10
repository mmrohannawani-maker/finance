from sqlalchemy.orm import Session
from app.models.analysis_model import Analysis
from app.schemas.analysis_schema import AnalysisCreate
import uuid
from sqlalchemy import desc
from typing import Optional

def create_analysis(db: Session, analysis: AnalysisCreate):
    db_analysis = Analysis(
        id=str(uuid.uuid4()),
        file_id=analysis.file_id,
        analysis_type=analysis.analysis_type,
        status=analysis.status
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

def get_analysis(db: Session, analysis_id: str):
    return db.query(Analysis).filter(Analysis.id == analysis_id).first()

def get_analyses_by_file(db: Session, file_id: str, skip: int = 0, limit: int = 100):
    return db.query(Analysis).filter(Analysis.file_id == file_id).offset(skip).limit(limit).all()

def update_analysis_status(db: Session, analysis_id: str, status: str):
    db_analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if db_analysis:
        db_analysis.status = status
        db.commit()
        db.refresh(db_analysis)
    return db_analysis

def update_analysis_results(db: Session, analysis_id: str, results: dict):
    from datetime import datetime
    db_analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if db_analysis:
        db_analysis.results = results
        db_analysis.status = "completed"
        db_analysis.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(db_analysis)
    return db_analysis


def get_analysis_by_file_and_type(
    db: Session, 
    file_id: str, 
    analysis_type: str,
    status: str = "completed"
) -> Optional[Analysis]:
    """Get specific completed analysis for a file and analysis type"""
    print(f"[CRUD] Getting {analysis_type} analysis for file {file_id}")
    return db.query(Analysis)\
        .filter(
            Analysis.file_id == file_id,
            Analysis.analysis_type == analysis_type,
            Analysis.status == status
        )\
        .order_by(desc(Analysis.created_at))\
        .first()

def get_latest_analysis(
    db: Session, 
    file_id: str, 
    status: str = "completed"
) -> Optional[Analysis]:
    """Get latest completed analysis for a file"""
    print(f"[CRUD] Getting latest analysis for file {file_id}")
    return db.query(Analysis)\
        .filter(
            Analysis.file_id == file_id,
            Analysis.status == status
        )\
        .order_by(desc(Analysis.created_at))\
        .first()