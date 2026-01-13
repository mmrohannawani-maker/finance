import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class File(Base):
    __tablename__ = "files"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    row_count = Column(Integer, default=0)
    column_count = Column(Integer, default=0)
    columns = Column(JSON, default=list)
    file_metadata = Column("metadata", JSON, default=dict)  # ✅ Column named "metadata" in DB
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<File {self.original_name}>"

class FileData(Base):
    __tablename__ = "file_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    row_index = Column(Integer, nullable=False, index=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<FileData {self.file_id} row {self.row_index}>"