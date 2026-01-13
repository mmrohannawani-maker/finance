import pandas as pd
import json
from typing import Dict, List, Tuple
import io
from fastapi import UploadFile

class CSVParser:
    @staticmethod
    async def parse_csv_content(content: bytes, filename: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Parse CSV from bytes content and return data and columns"""
        try:
            # Check if file is empty
            if not content or len(content) == 0:
                raise ValueError("CSV file is empty")
            
            # DEBUG: Print what we received
            print(f"DEBUG: Received {len(content)} bytes")
            try:
                content_str = content.decode('utf-8')[:200]
                print(f"DEBUG: First 200 chars: {content_str}")
            except:
                print(f"DEBUG: Content is not UTF-8 text")
            
            # Create BytesIO object from the content
            file_like_object = io.BytesIO(content)
            
            # Parse CSV using pandas FROM THE BYTESIO OBJECT
            df = pd.read_csv(file_like_object)
            
            # Check if pandas got valid data
            if df.empty:
                raise ValueError("CSV file contains no data rows")
                
            if len(df.columns) == 0:
                raise ValueError("No columns found in CSV file")
            
            # Convert to list of dictionaries
            data = df.to_dict(orient='records')
            
            # Get column names
            columns = df.columns.tolist()
            
            print(f"DEBUG: Parsed {len(data)} rows with columns: {columns}")
            
            return data, columns
            
        except pd.errors.EmptyDataError:
            raise ValueError("CSV file is empty or has no valid data")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing CSV: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error parsing CSV: {str(e)}")
        

    @staticmethod
    async def parse_excel(file: UploadFile) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Parse Excel file and return data and columns"""
        try:
            content = await file.read()
            df = pd.read_excel(io.BytesIO(content))
            data = df.to_dict(orient='records')
            columns = df.columns.tolist()
            return data, columns
            
        except Exception as e:
            raise ValueError(f"Error parsing Excel: {str(e)}")
    
    @staticmethod
    async def parse_file(file: UploadFile) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Parse file based on extension"""
        filename = file.filename.lower()
        
        content = await file.read()

        try:
            if filename.endswith('.csv'):
                return await CSVParser.parse_csv_content(content,filename)
            elif filename.endswith(('.xlsx', '.xls')):
                return await CSVParser.parse_excel(content,filename)
            else:
                raise ValueError("Unsupported file format. Please upload CSV or Excel files.")
        except Exception as e:
            print(f"ERROR erfdh in parse_file: {str(e)}")
            raise