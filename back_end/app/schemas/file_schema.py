from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from uuid import UUID

class FileBase(BaseModel):
    original_name: str
    file_size: int
    row_count: int = 0
    column_count: int = 0
    columns: List[str] = []

class FileCreate(FileBase):
    file_path: str
    mime_type: str
    filename: str
    file_metadata: Dict[str, Any] = Field(default_factory=dict, alias="metadata")

class FileUpdate(BaseModel):
    file_metadata: Optional[Dict[str, Any]] = Field(None, alias="metadata")

class FileInDB(FileBase):
    id: UUID
    filename: str
    file_path: str
    mime_type: str
    file_metadata: Dict[str, Any] = Field(default_factory=dict, alias="metadata")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True  # This allows using the alias

class FileResponse(FileInDB):
    pass

# File Data Schemas remain the same
class FileDataBase(BaseModel):
    row_index: int
    data: Dict[str, Any]

class FileDataCreate(FileDataBase):
    file_id: UUID

class FileDataInDB(FileDataBase):
    id: UUID
    file_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

    
# Pagination Schemas
class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(50, ge=1, le=100)

class PaginatedResponse(BaseModel):
    data: List[Dict[str, Any]]
    file: FileResponse
    pagination: Dict[str, Any]

# Upload Response
class UploadResponse(BaseModel):
    message: str
    file: FileResponse

# List Response
class FileListResponse(BaseModel):
    files: List[FileResponse]
    total: int
    page: int
    limit: int
    total_pages: int
