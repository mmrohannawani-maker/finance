from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime

class AnalysisBase(BaseModel):
    file_id: str
    analysis_type: str  # "summary", "trend", "correlation"
    status: str = "pending"  # pending, running, completed, failed

class AnalysisCreate(AnalysisBase):
    pass

class Analysis(AnalysisBase):
    id: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    results: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True

# Specific result schemas
class SummaryStats(BaseModel):
    column_name: str
    data_type: str
    count: int
    unique: int
    missing: int
    mean: Optional[float] = None
    median: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    std: Optional[float] = None

class TrendAnalysis(BaseModel):
    time_column: str
    value_column: str
    trend: str  # increasing, decreasing, stable, seasonal
    slope: Optional[float] = None
    seasonality_period: Optional[str] = None

class CorrelationResult(BaseModel):
    column_a: str
    column_b: str
    correlation: float
    strength: str  # weak, moderate, strong

# Add this to the END of your existing analysis_schema.py
class ReportRequest(BaseModel):
    """Schema for report generation request"""
    file_id: str
    analysis_type: str  # "summary", "trend", "correlation"