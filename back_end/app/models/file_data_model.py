import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class FileData(Base):
    __tablename__ = "file_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey('files.id', ondelete='CASCADE'), nullable=False, index=True)
    row_index = Column(Integer, nullable=False, index=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())  # ⭐ CHANGED: Removed timezone=True
    
    file = relationship("File", back_populates="data_rows")
    
    def __repr__(self):
        return f"<FileData {self.file_id} row {self.row_index}>"