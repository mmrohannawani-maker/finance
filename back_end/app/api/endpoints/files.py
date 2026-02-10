import os
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Create if doesn't exist
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from app.models import File
from app.services.file_service import FileService
from sqlalchemy.orm import Session
from app.services.openrouter_service import OpenRouterService
# Add this import in app/api/endpoints/files.py
from app.services.csv_parser import CSVParser
from app.schemas.file_schema import (
    FileResponse, FileListResponse, UploadResponse,
    PaginatedResponse, PaginationParams
)
from app.config import settings

# ✅ ADD THESE IMPORTS FOR CSV DATA SAVING
import pandas as pd
from app.crud.file_data_crud import create_bulk_file_data
from app.schemas.file_data_schema import FileDataCreate

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

    print("DEBUG 1: Starting upload endpoint")
    
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )

    # Validate file type
    allowed_extensions = settings.ALLOWED_FILE_TYPES
    file_ext = os.path.splitext(file.filename)[1].lower().lstrip(".")

    print(f"DEBUG 2: File extension: {file_ext}")
    print(f"DEBUG 3: Allowed extensions: {allowed_extensions}")
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Validate file size
    max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    content = await file.read()
    print(f"DEBUG 4: File size: {len(content)} bytes")
    if len(content) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE_MB}MB"
        )
    
    # Test read
    print(f"DEBUG 5: Content preview (first 100 bytes): {content[:100]}")
    
    # Reset file pointer
    await file.seek(0)

    data, columns = await CSVParser.parse_csv_content(content, file.filename)
    print(f"DEBUG 6: CSV parsed. Rows: {len(data)}, Columns: {columns}")
    
    try:
        # Process and save file
        print("DEBUG 7: Calling file_service.process_and_save_file()")
        file_record = await file_service.process_and_save_file(db, file)
        print(f"DEBUG 8: File processed successfully. File ID: {file_record.id}")
        
        # ✅ ADDED: Save CSV data to database
        print(f"DEBUG 9: Starting CSV data save to database...")
        await save_csv_data(content, str(file_record.id), db)
        print(f"DEBUG 10: CSV data saved to database successfully!")
        
        return UploadResponse(
            message="File uploaded successfully",
            file=FileResponse.from_orm(file_record)
        )
    
    except Exception as e:
        print(f"DEBUG ERROR: Exception in upload endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ✅ ADDED FUNCTION: Save CSV data to database
async def save_csv_data(file_content: bytes, file_id: str, db: AsyncSession):
    """Parse CSV and save to database"""
    print(f"DEBUG save_csv_data 1: Starting to save CSV data for file_id: {file_id}")
    
    try:
        # Convert bytes to file-like object for pandas
        import io
        file_like = io.BytesIO(file_content)
        
        # Read CSV
        print(f"DEBUG save_csv_data 2: Reading CSV with pandas...")
        df = pd.read_csv(file_like)
        print(f"DEBUG save_csv_data 3: CSV read. Shape: {df.shape}, Columns: {list(df.columns)}")
        
        # Prepare data for bulk insert
        file_data_list = []
        print(f"DEBUG save_csv_data 4: Preparing {len(df)} rows for database...")
        
        for idx, row in df.iterrows():
            file_data = FileDataCreate(
                file_id=file_id,
                row_index=int(idx),
                row_data=row.to_dict()
            )
            file_data_list.append(file_data)
            
            # Print first 3 rows for debugging
            if idx < 3:
                print(f"DEBUG save_csv_data 5: Row {idx} sample: {row.to_dict()}")
        
        print(f"DEBUG save_csv_data 6: Saving {len(file_data_list)} rows to database via bulk insert...")
        
        # Save to database
        # Note: We need to use synchronous session for CRUD operations
        from app.database import SessionLocal
        sync_db = SessionLocal()
        try:
            created_rows = create_bulk_file_data(sync_db, file_data_list)
            print(f"DEBUG save_csv_data 7: Successfully saved {len(created_rows)} rows to database")
        finally:
            sync_db.close()
        
    except Exception as e:
        print(f"ERROR save_csv_data: Failed to save CSV data: {str(e)}")
        import traceback
        traceback.print_exc()
        # Don't raise - just log, so file upload still succeeds
        print(f"WARNING: CSV data not saved to database, but file upload succeeded")

@router.get("/", response_model=FileListResponse)
async def get_files(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all uploaded files with pagination"""
    print(f"DEBUG get_files: Page: {page}, Limit: {limit}")
    try:
        skip = (page - 1) * limit
        files = await file_service.get_all_files(db, skip, limit)
        total = await file_service.get_file_count(db)
        
        print(f"DEBUG get_files: Found {len(files)} files, Total: {total}")
        
        return FileListResponse(
            files=[FileResponse.from_orm(file) for file in files],
            total=total,
            page=page,
            limit=limit,
            total_pages=(total + limit - 1) // limit
        )
        
    except Exception as e:
        print(f"ERROR get_files: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Get file details by ID"""
    print(f"DEBUG get_file: Getting file with ID: {file_id}")
    file = await file_service.get_file_by_id(db, file_id)
    if not file:
        print(f"DEBUG get_file: File not found: {file_id}")
        raise HTTPException(status_code=404, detail="File not found")
    
    print(f"DEBUG get_file: Found file: {file.filename}")
    return FileResponse.from_orm(file)

@router.get("/{file_id}/data", response_model=PaginatedResponse)
async def get_file_data(
    file_id: UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_async_db)
):
    """Get paginated data from a file"""
    print(f"DEBUG get_file_data: File ID: {file_id}, Page: {page}, Limit: {limit}")
    try:
        skip = (page - 1) * limit
        result = await file_service.get_file_data(db, file_id, skip, limit)
        
        print(f"DEBUG get_file_data: Got {len(result['data'])} rows")
        
        return PaginatedResponse(
            file=FileResponse.from_orm(result["file"]),
            data=result["data"],
            pagination=result["pagination"]
        )
        
    except ValueError as e:
        print(f"DEBUG get_file_data: ValueError - {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"ERROR get_file_data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{file_id}")
async def delete_file(
    file_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Delete a file and its data"""
    print(f"DEBUG delete_file: Deleting file with ID: {file_id}")
    success = await file_service.delete_file(db, file_id)
    if not success:
        print(f"DEBUG delete_file: File not found: {file_id}")
        raise HTTPException(status_code=404, detail="File not found")
    
    print(f"DEBUG delete_file: Successfully deleted file: {file_id}")
    return {"message": "File deleted successfully"}

@router.post("/{file_id}/analyze")
async def analyze_file_data(
    file_id: UUID,
    query: str = Query(None, description="Optional custom analysis query"),
    db: AsyncSession = Depends(get_async_db)
):
    """Analyze file data using AI"""
    print(f"DEBUG analyze_file_data: File ID: {file_id}, Query: {query}")
    try:
        # Get file data (first 100 rows for analysis)
        result = await file_service.get_file_data(db, file_id, skip=0, limit=100)
        data = result["data"]
        
        print(f"DEBUG analyze_file_data: Got {len(data)} rows for analysis")
        
        if not data:
            raise HTTPException(status_code=400, detail="No data available for analysis")
        
        # Analyze with OpenRouter
        print(f"DEBUG analyze_file_data: Calling OpenRouter service...")
        analysis = await openrouter_service.analyze_data(data, query)
        
        print(f"DEBUG analyze_file_data: Analysis completed successfully")
        
        return {
            "file_id": file_id,
            "analysis": analysis,
            "rows_analyzed": len(data)
        }
        
    except ValueError as e:
        print(f"DEBUG analyze_file_data: ValueError - {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"ERROR analyze_file_data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{file_id}/chart-suggestions")
async def get_chart_suggestions(
    file_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Get AI suggestions for chart types"""
    print(f"DEBUG get_chart_suggestions: File ID: {file_id}")
    try:
        # Get file and sample data
        file = await file_service.get_file_by_id(db, file_id)
        if not file:
            print(f"DEBUG get_chart_suggestions: File not found")
            raise HTTPException(status_code=404, detail="File not found")
        
        print(f"DEBUG get_chart_suggestions: Found file: {file.filename}")
        
        result = await file_service.get_file_data(db, file_id, skip=0, limit=5)
        data_sample = result["data"]
        
        print(f"DEBUG get_chart_suggestions: Got {len(data_sample)} sample rows")
        
        # Get chart suggestions
        print(f"DEBUG get_chart_suggestions: Calling OpenRouter for chart suggestions...")
        suggestions = await openrouter_service.generate_chart_suggestions(
            file.columns, 
            data_sample
        )
        
        print(f"DEBUG get_chart_suggestions: Got {len(suggestions)} suggestions")
        
        return {
            "file_id": file_id,
            "columns": file.columns,
            "suggestions": suggestions
        }
        
    except Exception as e:
        print(f"ERROR get_chart_suggestions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
