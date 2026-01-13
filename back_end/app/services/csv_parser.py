import pandas as pd
import json
from typing import Dict, List, Tuple
import io
from fastapi import UploadFile

class CSVParser:
    @staticmethod
    async def parse_csv(file: UploadFile) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Parse CSV file and return data and columns"""
        try:
            # Read file content
            content = await file.read()
            
            # Parse CSV using pandas
            df = pd.read_csv(io.BytesIO(content))
            
            # Convert to list of dictionaries
            data = df.to_dict(orient='records')
            
            # Get column names
            columns = df.columns.tolist()
            
            return data, columns
            
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
        
        if filename.endswith('.csv'):
            return await CSVParser.parse_csv(file)
        elif filename.endswith(('.xlsx', '.xls')):
            return await CSVParser.parse_excel(file)
        else:
            raise ValueError("Unsupported file format. Please upload CSV or Excel files.")
