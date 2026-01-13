import os
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from app.services.file_service import FileService
from app.services.openrouter_service import OpenRouterService
from app.schemas.file_schema import (
    FileResponse, FileListResponse, UploadResponse,
    PaginatedResponse, PaginationParams
)
from app.config import settings

router = APIRouter(prefix="/files", tags=["files"])

# Initialize services
file_service = FileService(settings.UPLOAD_DIR)
openrouter_service = OpenRouterService()

@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    db: AsyncSession = Depends(get_async_db)
):
    """Upload and process a CSV/Excel file"""
    
    # Validate file type
    allowed_extensions = settings.ALLOWED_FILE_TYPES
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Validate file size
    max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    content = await file.read()
    if len(content) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE_MB}MB"
        )
    
    # Reset file pointer
    await file.seek(0)
    
    try:
        # Process and save file
        file_record = await file_service.process_and_save_file(db, file)
        
        return UploadResponse(
            message="File uploaded successfully",
            file=FileResponse.from_orm(file_record)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=FileListResponse)
async def get_files(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all uploaded files with pagination"""
    try:
        skip = (page - 1) * limit
        files = await file_service.get_all_files(db, skip, limit)
        total = await file_service.get_file_count(db)
        
        return FileListResponse(
            files=[FileResponse.from_orm(file) for file in files],
            total=total,
            page=page,
            limit=limit,
            total_pages=(total + limit - 1) // limit
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Get file details by ID"""
    file = await file_service.get_file_by_id(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse.from_orm(file)

@router.get("/{file_id}/data", response_model=PaginatedResponse)
async def get_file_data(
    file_id: UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_async_db)
):
    """Get paginated data from a file"""
    try:
        skip = (page - 1) * limit
        result = await file_service.get_file_data(db, file_id, skip, limit)
        
        return PaginatedResponse(
            file=FileResponse.from_orm(result["file"]),
            data=result["data"],
            pagination=result["pagination"]
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{file_id}")
async def delete_file(
    file_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Delete a file and its data"""
    success = await file_service.delete_file(db, file_id)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {"message": "File deleted successfully"}

@router.post("/{file_id}/analyze")
async def analyze_file_data(
    file_id: UUID,
    query: str = Query(None, description="Optional custom analysis query"),
    db: AsyncSession = Depends(get_async_db)
):
    """Analyze file data using AI"""
    try:
        # Get file data (first 100 rows for analysis)
        result = await file_service.get_file_data(db, file_id, skip=0, limit=100)
        data = result["data"]
        
        if not data:
            raise HTTPException(status_code=400, detail="No data available for analysis")
        
        # Analyze with OpenRouter
        analysis = await openrouter_service.analyze_data(data, query)
        
        return {
            "file_id": file_id,
            "analysis": analysis,
            "rows_analyzed": len(data)
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{file_id}/chart-suggestions")
async def get_chart_suggestions(
    file_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Get AI suggestions for chart types"""
    try:
        # Get file and sample data
        file = await file_service.get_file_by_id(db, file_id)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        
        result = await file_service.get_file_data(db, file_id, skip=0, limit=5)
        data_sample = result["data"]
        
        # Get chart suggestions
        suggestions = await openrouter_service.generate_chart_suggestions(
            file.columns, 
            data_sample
        )
        
        return {
            "file_id": file_id,
            "columns": file.columns,
            "suggestions": suggestions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
