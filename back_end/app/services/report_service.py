# # app/services/report_service.py
# import os
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib import colors
# from reportlab.lib.units import inch
# import tempfile
# from typing import Dict, Any, List

# class ReportService:
#     def __init__(self):
#         self.styles = getSampleStyleSheet()
#         # DON'T call create_custom_styles() here if it's causing errors
#         # self.create_custom_styles()
    
#     def create_custom_styles(self):
#         """Create custom styles for the report - ONLY if they don't exist"""
#         try:
#             # Check if style already exists before adding
#             if 'Title' not in self.styles.byName:
#                 self.styles.add(ParagraphStyle(
#                     name='Title',
#                     parent=self.styles['Heading1'],
#                     fontSize=24,
#                     spaceAfter=30,
#                     alignment=1  # Center
#                 ))
            
#             if 'Heading2' not in self.styles.byName:
#                 self.styles.add(ParagraphStyle(
#                     name='Heading2',
#                     parent=self.styles['Heading2'],  # This might be the issue
#                     fontSize=14,
#                     spaceAfter=12,
#                     spaceBefore=20
#                 ))
#         except Exception as e:
#             print(f"[WARNING] Could not create custom styles: {e}")
#             # Use existing styles
    
#     def create_pdf_report(self, analysis_results: Dict[str, Any], analysis_type: str) -> str:
#         """Create PDF from analysis results"""
#         print(f"[DEBUG] Creating PDF for {analysis_type} analysis")
        
#         # Create temporary PDF file
#         pdf_path = tempfile.mktemp(suffix=".pdf")
#         print(f"[DEBUG] PDF will be saved to: {pdf_path}")
        
#         # Create document
#         doc = SimpleDocTemplate(pdf_path, pagesize=letter)
#         story = []
        
#         # Title - use existing Heading1 style
#         title = f"Financial Analysis Report - {analysis_type.title()} Analysis"
#         story.append(Paragraph(title, self.styles['Heading1']))
#         story.append(Spacer(1, 0.25*inch))
        
#         # Add analysis results based on type
#         if analysis_type == "summary":
#             self._add_summary_results(story, analysis_results)
#         elif analysis_type == "trend":
#             self._add_trend_results(story, analysis_results)
#         elif analysis_type == "correlation":
#             self._add_correlation_results(story, analysis_results)
        
#         # Build PDF
#         doc.build(story)
#         print(f"[DEBUG] PDF created successfully at: {pdf_path}")
        
#         return pdf_path
    
#     def _add_summary_results(self, story: List, results: Dict[str, Any]):
#         """Add summary statistics to PDF"""
#         print("[DEBUG] Adding summary results to PDF")
        
#         # Use Heading2 style that already exists
#         story.append(Paragraph("Summary Statistics", self.styles['Heading2']))
        
#         if "columns" not in results:
#             story.append(Paragraph("No summary data available", self.styles['Normal']))
#             return
        
#         for col_info in results.get("columns", [])[:10]:  # Limit to first 10 columns
#             story.append(Paragraph(f"<b>Column:</b> {col_info.get('name', 'N/A')}", self.styles['Normal']))
            
#             # Add basic info
#             text = f"Type: {col_info.get('dtype', 'N/A')} | "
#             text += f"Count: {col_info.get('count', 0)} | "
#             text += f"Unique: {col_info.get('unique', 0)} | "
#             text += f"Missing: {col_info.get('missing', 0)}"
#             story.append(Paragraph(text, self.styles['Normal']))
            
#             # Add numeric stats if available
#             if "mean" in col_info:
#                 num_text = f"Mean: {col_info.get('mean', 0):.2f} | "
#                 num_text += f"Min: {col_info.get('min', 0):.2f} | "
#                 num_text += f"Max: {col_info.get('max', 0):.2f} | "
#                 num_text += f"Std: {col_info.get('std', 0):.2f}"
#                 story.append(Paragraph(num_text, self.styles['Normal']))
            
#             story.append(Spacer(1, 0.1*inch))
    
#     def _add_trend_results(self, story: List, results: Dict[str, Any]):
#         """Add trend analysis to PDF"""
#         print(f"[REPORT DEBUG] Trend results type: {type(results)}")
#         print(f"[REPORT DEBUG] Trend results keys: {results.keys() if isinstance(results, dict) else 'Not a dict'}")
    
#         story.append(Paragraph("Trend Analysis", self.styles['Heading2']))
    
#     # Check for "error" key first
#         if "error" in results:
#             story.append(Paragraph(f"Error: {results['error']}", self.styles['Normal']))
#             return
    
#         # Check for trends in results (directly or nested)
#         trends_data = None
    
#         # Case 1: Results is the trends dict directly
#         if "trends" in results:
#             trends_data = results.get("trends", [])
#             print(f"[REPORT DEBUG] Found trends in 'trends' key: {len(trends_data)} items")
    
#         # Case 2: Results IS the trends list
#         elif isinstance(results, list):
#             trends_data = results
#             print(f"[REPORT DEBUG] Results is a list: {len(trends_data)} items")
    
#         # Case 3: Look for any list in results
#         else:
#             for key, value in results.items():
#                 if isinstance(value, list):
#                     trends_data = value
#                     print(f"[REPORT DEBUG] Found list in key '{key}': {len(trends_data)} items")
#                     break
    
#         if not trends_data:
#             story.append(Paragraph("No trend data available", self.styles['Normal']))
#             return
    
#         # Create table
#         table_data = [["Date Column", "Value Column", "Slope", "Trend", "Data Points"]]
    
#         for trend in trends_data[:10]:  # Limit to 10
#             row = [
#                 str(trend.get("date_column", "N/A")),
#                 str(trend.get("value_column", "N/A")),
#                 f"{trend.get('slope', 0):.6f}",
#                 str(trend.get("trend", "N/A")),
#                 str(trend.get("data_points", 0))
#             ]
#             table_data.append(row)
    
#         # Create table if we have data
#         if len(table_data) > 1:
#             table = Table(table_data, colWidths=[1.2*inch, 1.2*inch, 1*inch, 0.8*inch, 0.8*inch])
#             table.setStyle(TableStyle([
#                 ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                 ('FONTSIZE', (0, 0), (-1, 0), 10),
#                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                 ('GRID', (0, 0), (-1, -1), 1, colors.black)
#             ]))
#             story.append(table)
#         else:
#             story.append(Paragraph("No trend data available", self.styles['Normal']))
    
#     def _add_correlation_results(self, story: List, results: Dict[str, Any]):
#         """Add correlation analysis to PDF"""
#         print(f"[REPORT DEBUG] Correlation results type: {type(results)}")
#         print(f"[REPORT DEBUG] Correlation results keys: {results.keys() if isinstance(results, dict) else 'Not a dict'}")
    
#         story.append(Paragraph("Correlation Analysis", self.styles['Heading2']))
    
#         # Check for "error" key first
#         if "error" in results:
#             story.append(Paragraph(f"Error: {results['error']}", self.styles['Normal']))
#             return
    
#         # Check for correlations
#         corr_data = None
    
#         if "correlations" in results:
#             corr_data = results.get("correlations", [])
#             print(f"[REPORT DEBUG] Found correlations in 'correlations' key: {len(corr_data)} items")
#         elif isinstance(results, list):
#             corr_data = results
#             print(f"[REPORT DEBUG] Results is a list: {len(corr_data)} items")
#         else:
#             for key, value in results.items():
#                 if isinstance(value, list):
#                     corr_data = value
#                     print(f"[REPORT DEBUG] Found list in key '{key}': {len(corr_data)} items")
#                     break
    
#         if not corr_data:
#             story.append(Paragraph("No correlation data available", self.styles['Normal']))
#             return
    
#     # Create table
#     table_data = [["Column A", "Column B", "Correlation", "Strength", "Interpretation"]]
    
#     for corr in corr_data[:15]:  # Limit to 15
#         row = [
#             str(corr.get("column_a", "N/A")),
#             str(corr.get("column_b", "N/A")),
#             f"{corr.get('correlation', 0):.3f}",
#             str(corr.get("strength", "N/A")),
#             str(corr.get("interpretation", "N/A"))
#         ]
#         table_data.append(row)
    
#     if len(table_data) > 1:
#         table = Table(table_data, colWidths=[1*inch, 1*inch, 0.8*inch, 0.8*inch, 1.4*inch])
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('FONTSIZE', (0, 0), (-1, 0), 10),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#             ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black)
#         ]))
#         story.append(table)
#     else:
#         story.append(Paragraph("No correlation data available", self.styles['Normal']))