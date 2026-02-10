// src/data/hooks/useReportGenerator.ts
import { useState } from 'react';

export const useReportGenerator = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateReport = async (fileId: string, analysisType: string) => {
    setIsGenerating(true);
    setError(null);
    
    try {
      console.log(`Generating ${analysisType} report for file ${fileId}`);
      
      const response = await fetch('http://localhost:8000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          file_id: fileId,
          analysis_type: analysisType
        })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate report');
      }
      
      // Create and download blob
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${analysisType}_report.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      console.log('Report downloaded successfully');
      return true;
      
    } catch (err: any) {
      console.error('Error generating report:', err);
      setError(err.message || 'Failed to generate report');
      return false;
    } finally {
      setIsGenerating(false);
    }
  };

  return {
    generateReport,
    isGenerating,
    error,
    clearError: () => setError(null)
  };
};