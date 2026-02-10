import pandas as pd
import numpy as np
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from app.crud.analysis_crud import create_analysis, update_analysis_results, update_analysis_status
from app.crud.file_data_crud import get_file_data
from app.schemas.analysis_schema import AnalysisCreate
import uuid
import asyncio

class AnalysisService:
    def __init__(self, db: Session):
        self.db = db

    def _convert_filedata_to_dataframe(self, file_data_list):
        """Convert FileData objects to pandas DataFrame"""
        if not file_data_list:
            return pd.DataFrame()
    
        print(f"[DEBUG] Converting {len(file_data_list)} FileData records")
    
        # Each FileData has: row_index, data (JSON dict)
        # data contains: {'Date': '2000-01-01', 'Stock Index': 'Dow Jones', ...}
    
        rows_dict = {}
    
        for item in file_data_list:
            row_idx = item.row_index
        
            if row_idx not in rows_dict:
                rows_dict[row_idx] = {}
        
            # Get the JSON data dict
            if item.data:
                # item.data is already a dictionary like:
                # {'Date': '2000-01-01', 'Stock Index': 'Dow Jones', 'Open Price': 2128.75, ...}
                rows_dict[row_idx] = item.data.copy()
    
        # Convert to DataFrame
        df = pd.DataFrame.from_dict(rows_dict, orient='index')
    
        print(f"[DEBUG] DataFrame created: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"[DEBUG] Columns: {list(df.columns)}")
    
        return df.sort_index()
    





    
    def start_analysis(self, file_id: str, analysis_type: str):
        """Start a new analysis and return analysis ID"""
        analysis_create = AnalysisCreate(
            file_id=file_id,
            analysis_type=analysis_type,
            status="running"
        )
        analysis = create_analysis(self.db, analysis_create)
        
        # Run analysis asynchronously
        asyncio.create_task(self.run_analysis(analysis.id, file_id, analysis_type))
        
        return analysis
    
    async def run_analysis(self, analysis_id: str, file_id: str, analysis_type: str):
        """Run the actual analysis"""
        try:
            print(f"[ANALYSIS] Starting {analysis_type} analysis...")
        
            # Get file data
            file_data = get_file_data(self.db, file_id, limit=1000)
            print(f"[ANALYSIS] Got {len(file_data)} FileData records")
        
            if not file_data:
                print("[ANALYSIS ERROR] No data found")
                update_analysis_status(self.db, analysis_id, "failed")
                return
        
            # Convert to DataFrame - SIMPLE NOW!
            # Each FileData has .data which is a dict
            df = self._convert_filedata_to_dataframe(file_data)
        
            if df.empty:
                print("[ANALYSIS ERROR] DataFrame empty")
                update_analysis_status(self.db, analysis_id, "failed")
                return
        
            print(f"[ANALYSIS] Data shape: {df.shape}")
        
            # Run analysis
            if analysis_type == "summary":
                results = self.summary_statistics(df)
            elif analysis_type == "trend":
                results = self.trend_analysis(df)
            elif analysis_type == "correlation":
                results = self.correlation_analysis(df)
            else:
                print(f"[ANALYSIS ERROR] Unknown type: {analysis_type}")
                update_analysis_status(self.db, analysis_id, "failed")
                return
        
            print(f"[ANALYSIS] Analysis complete, saving...")
        
            # Save results
            update_analysis_results(self.db, analysis_id, results)
            print(f"[ANALYSIS] SUCCESS - Analysis {analysis_id} completed!")
        
        except Exception as e:
            print(f"[ANALYSIS ERROR] Exception: {str(e)}")
            import traceback
            traceback.print_exc()
            update_analysis_status(self.db, analysis_id, "failed")


            
    def summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate summary statistics for all columns"""
        results = {"columns": []}
        
        for column in df.columns:
            col_data = df[column]
            col_info = {
                "name": column,
                "dtype": str(col_data.dtype),
                "count": int(len(col_data)),  # Convert to int
                "unique": int(col_data.nunique()),  # Convert to int
                "missing": int(col_data.isnull().sum())  # Convert to int
            }
            
            # Numeric statistics
            if pd.api.types.is_numeric_dtype(col_data):
                col_info.update({
                    "mean": float(col_data.mean()),
                    "median": float(col_data.median()),
                    "min": float(col_data.min()),
                    "max": float(col_data.max()),
                    "std": float(col_data.std()),
                    "q1": float(col_data.quantile(0.25)),
                    "q3": float(col_data.quantile(0.75))
                })
            
            # String statistics
            elif pd.api.types.is_string_dtype(col_data):
                mode_result = col_data.mode()
                most_common = str(mode_result.iloc[0]) if not mode_result.empty else None
                avg_length = float(col_data.str.len().mean()) if not col_data.empty else None
            
                col_info.update({
                    "most_common": most_common,
                    "avg_length": avg_length
                })
        
            results["columns"].append(col_info)
    
        return results
    





    
    def trend_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze trends in time series data"""
        results = {"trends": []}
        
        # Find date columns
        date_columns = []
        for col in df.columns:
            try:
                pd.to_datetime(df[col], errors='raise')
                date_columns.append(col)
            except:
                continue
        
        if not date_columns:
            return {"error": "No date columns found for trend analysis"}
        
        # Find numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_columns:
            return {"error": "No numeric columns found for trend analysis"}
        
        # Analyze trends for each date-numeric combination
        for date_col in date_columns[:1]:  # Just use first date column
            df_sorted = df.sort_values(date_col)
            for num_col in numeric_columns[:3]:  # Limit to first 3 numeric columns
                try:
                    # Simple linear trend
                    x = pd.to_numeric(pd.to_datetime(df_sorted[date_col]))
                    y = df_sorted[num_col].astype(float)
                    
                    # Remove NaN
                    mask = ~(np.isnan(x) | np.isnan(y))
                    x_clean = x[mask]
                    y_clean = y[mask]
                    
                    if len(x_clean) > 1:
                        # Linear regression
                        coeffs = np.polyfit(x_clean, y_clean, 1)
                        slope = coeffs[0]
                        
                        trend_info = {
                            "date_column": date_col,
                            "value_column": num_col,
                            "slope": float(slope),
                            "trend": "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable",
                            "data_points": int(len(x_clean))
                        }
                        results["trends"].append(trend_info)
                except:
                    continue
        
        return results
    
    def correlation_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate correlation matrix for numeric columns"""
        results = {"correlations": []}
        
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty or len(numeric_df.columns) < 2:
            return {"error": "Need at least 2 numeric columns for correlation analysis"}
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        # Get strong correlations (abs > 0.7)
        strong_corrs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr = corr_matrix.iloc[i, j]
                if abs(corr) > 0.3:  # Include moderate correlations
                    col1 = corr_matrix.columns[i]
                    col2 = corr_matrix.columns[j]
                    
                    # Determine strength
                    abs_corr = abs(corr)
                    if abs_corr > 0.7:
                        strength = "strong"
                    elif abs_corr > 0.4:
                        strength = "moderate"
                    else:
                        strength = "weak"
                    
                    strong_corrs.append({
                        "column_a": col1,
                        "column_b": col2,
                        "correlation": float(corr),
                        "strength": strength,
                        "interpretation": self.get_correlation_interpretation(corr)
                    })
        
        # Sort by absolute correlation
        strong_corrs.sort(key=lambda x: abs(x["correlation"]), reverse=True)
        
        results["correlations"] = strong_corrs[:10]  # Top 10
        return results
    
    def get_correlation_interpretation(self, corr: float) -> str:
        """Get human-readable interpretation of correlation"""
        abs_corr = abs(corr)
        
        if abs_corr > 0.8:
            return "Very strong relationship"
        elif abs_corr > 0.6:
            return "Strong relationship"
        elif abs_corr > 0.4:
            return "Moderate relationship"
        elif abs_corr > 0.2:
            return "Weak relationship"
        else:
            return "Very weak or no relationship"