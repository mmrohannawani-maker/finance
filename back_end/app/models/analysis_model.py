from sqlalchemy import Column, String, DateTime, JSON, Text
from sqlalchemy.sql import func
from app.database import Base

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(String, primary_key=True, index=True)
    file_id = Column(String, index=True, nullable=False)
    analysis_type = Column(String, nullable=False)  # summary, trend, correlation
    status = Column(String, default="pending")  # pending, running, completed, failed
    results = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)