import os
import shutil
from typing import List, Dict, Any, Optional
from uuid import UUID
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from app.models.file_model import File, FileData
from app.schemas.file_schema import FileCreate, FileDataCreate
from app.services.csv_parser import CSVParser

class FileService:
    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)
    
    async def save_uploaded_file(self, file: UploadFile) -> str:
        """Save uploaded file to disk and return file path"""
        # Generate unique filename
        import time
        timestamp = int(time.time() * 1000)
        unique_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(self.upload_dir, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return file_path, unique_filename
    
    async def process_and_save_file(
        self, 
        db: AsyncSession, 
        file: UploadFile
    ) -> File:
        """Process uploaded file and save to database"""
        
        # 1. Save file to disk
        file_path, filename = await self.save_uploaded_file(file)
        
        # 2. Parse file content
        data, columns = await CSVParser.parse_file(file)
        
        # 3. Create File record
        file_record = File(
            filename=filename,
            original_name=file.filename,
            file_path=file_path,
            file_size=os.path.getsize(file_path),
            mime_type=file.content_type or "application/octet-stream",
            row_count=len(data),
            column_count=len(columns),
            columns=columns,
            file_metadata={  # ✅ Use file_metadata instead of metadata
            "field_name": file.filename,
            "content_type": file.content_type
            }
        )
        
        db.add(file_record)
        await db.commit()
        await db.refresh(file_record)
        
        # 4. Create FileData records
        file_data_records = [
            FileData(
                file_id=file_record.id,
                row_index=index,
                data=row
            )
            for index, row in enumerate(data)
        ]
        
        db.add_all(file_data_records)
        await db.commit()
        
        return file_record
    
    async def get_all_files(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[File]:
        """Get all files with pagination"""
        result = await db.execute(
            select(File)
            .order_by(File.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_file_by_id(
        self, 
        db: AsyncSession, 
        file_id: UUID
    ) -> Optional[File]:
        """Get file by ID"""
        result = await db.execute(
            select(File).where(File.id == file_id)
        )
        return result.scalar_one_or_none()
    
    async def get_file_data(
        self,
        db: AsyncSession,
        file_id: UUID,
        skip: int = 0,
        limit: int = 50
    ) -> Dict[str, Any]:
        """Get paginated file data"""
        # Get file
        file = await self.get_file_by_id(db, file_id)
        if not file:
            raise ValueError("File not found")
        
        # Get total count
        total_count = await db.scalar(
            select(func.count(FileData.id))
            .where(FileData.file_id == file_id)
        )
        
        # Get paginated data
        result = await db.execute(
            select(FileData)
            .where(FileData.file_id == file_id)
            .order_by(FileData.row_index)
            .offset(skip)
            .limit(limit)
        )
        
        file_data = result.scalars().all()
        
        return {
            "file": file,
            "data": [row.data for row in file_data],
            "pagination": {
                "page": skip // limit + 1,
                "limit": limit,
                "total": total_count,
                "pages": (total_count + limit - 1) // limit
            }
        }
    
    async def delete_file(
        self,
        db: AsyncSession,
        file_id: UUID
    ) -> bool:
        """Delete file and its data"""
        # Get file
        file = await self.get_file_by_id(db, file_id)
        if not file:
            return False
        
        # Delete file from disk
        if os.path.exists(file.file_path):
            os.remove(file.file_path)
        
        # Delete FileData records
        await db.execute(
            delete(FileData).where(FileData.file_id == file_id)
        )
        
        # Delete File record
        await db.delete(file)
        await db.commit()
        
        return True
    
    async def get_file_count(self, db: AsyncSession) -> int:
        """Get total number of files"""
        result = await db.scalar(select(func.count(File.id)))
        return result or 0 
