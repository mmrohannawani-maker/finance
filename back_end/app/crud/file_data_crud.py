from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.models.file_data_model import FileData
from app.schemas.file_data_schema import FileDataCreate

def _ensure_uuid(file_id):
    """Convert string to UUID if needed"""
    if isinstance(file_id, str):
        try:
            return UUID(file_id)
        except ValueError:
            return file_id  # Return as-is if not a valid UUID string
    return file_id

def get_file_data(db: Session, file_id: str, skip: int = 0, limit: int = 1000) -> List[FileData]:
    """Get file data records for a specific file"""
    file_uuid = _ensure_uuid(file_id)
    return db.query(FileData).filter(FileData.file_id == file_uuid).order_by(FileData.row_index).offset(skip).limit(limit).all()

def create_file_data(db: Session, file_data: FileDataCreate) -> FileData:
    """Create new file data record"""
    # Convert file_id string to UUID if needed
    data_dict = file_data.dict()
    data_dict['file_id'] = _ensure_uuid(data_dict['file_id'])
    
    db_file_data = FileData(**data_dict)
    db.add(db_file_data)
    db.commit()
    db.refresh(db_file_data)
    return db_file_data

def create_bulk_file_data(db: Session, file_data_list: List[FileDataCreate]) -> List[FileData]:
    """Create multiple file data records at once"""
    db_file_data_list = []
    for data in file_data_list:
        data_dict = data.dict()
        data_dict['file_id'] = _ensure_uuid(data_dict['file_id'])
        db_file_data_list.append(FileData(**data_dict))
    
    db.add_all(db_file_data_list)
    db.commit()
    return db_file_data_list

def delete_file_data(db: Session, file_id: str):
    """Delete all data for a file"""
    print(f"🔍 DEBUG delete_file_data: file_id={file_id}, type={type(file_id)}")
    
    file_uuid = _ensure_uuid(file_id)
    print(f"🔍 DEBUG: Converted to UUID: {file_uuid}, type={type(file_uuid)}")
    
    # Check how many rows will be deleted
    count = db.query(FileData).filter(FileData.file_id == file_uuid).count()
    print(f"🔍 DEBUG: Found {count} rows to delete")
    
    if count > 0:
        result = db.query(FileData).filter(FileData.file_id == file_uuid).delete()
        db.commit()
        print(f"✅ DEBUG: Deleted {result} rows")
    else:
        print("⚠️ DEBUG: No rows found to delete")
        db.commit()  # Still commit even if nothing to delete