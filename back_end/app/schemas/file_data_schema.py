# app/schemas/file_data_schema.py
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class FileDataBase(BaseModel):
    file_id: str  # UUID as string
    row_index: int
    data: Dict[str, Any]

class FileDataCreate(FileDataBase):
    pass

class FileData(FileDataBase):
    id: str  # UUID as string
    created_at: datetime
    
    class Config:
        orm_mode = True