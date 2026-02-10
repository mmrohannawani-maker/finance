import AnalysisSelector, { AnalysisType } from "@/components/AnalysisSelector";
import { useState } from "react";
import { Database, FileSpreadsheet, BarChart3, FileText, Download } from "lucide-react";
import FileUploadZone from "@/components/FileUploadZone";
import CSVFileCard from "@/components/CSVFileCard";
import { Button } from "@/components/ui/button";

import { useToast } from "@/hooks/use-toast";

const Index = () => {
   const { toast } = useToast(); // ← ADD THIS LINE
   const [refreshTrigger, setRefreshTrigger] = useState(0);
   const [selectedAnalysis, setSelectedAnalysis] = useState<AnalysisType>(null);
   const [selectedFileId, setSelectedFileId] = useState<string | null>(null); // ADD THIS LINE
   const [selectedFileName, setSelectedFileName] = useState<string>("");
   const handleFileUploadSuccess = () => {
    // Trigger refresh in CSVFileCard
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg gradient-header flex items-center justify-center">
              <Database className="w-5 h-5 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground">CSV Analytics</h1>
              <p className="text-sm text-muted-foreground">
                Upload, explore, and visualize your data
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container max-w-6xl mx-auto px-4 py-8">
        {/* Upload Section */}
        <section className="mb-8">
          <div className="analytics-card p-6">
            <h2 className="text-xl font-semibold text-foreground mb-4">
              Upload CSV File
            </h2>
            <FileUploadZone onUploadSuccess={handleFileUploadSuccess} />
          </div>
        </section>

        {/* Three Analysis Buttons Section
        <section className="mb-8">
          <div className="analytics-card p-6">
            <h2 className="text-xl font-semibold text-foreground mb-6">
              Data Analysis Tools
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Button 
                variant="default"
                className="flex flex-col items-center justify-center p-6 h-full bg-blue-600 hover:bg-blue-700"
              >
                <BarChart3 className="w-10 h-10 mb-3" />
                <span className="font-semibold">Analyze Data</span>
                <p className="text-sm text-muted-foreground mt-2">Generate insights and statistics</p>
              </Button>
              
              <Button 
                variant="secondary"
                className="flex flex-col items-center justify-center p-6 h-full bg-purple-600 hover:bg-purple-700 text-white"
              >
                <FileText className="w-10 h-10 mb-3" />
                <span className="font-semibold">Generate Report</span>
                <p className="text-sm text-white/80 mt-2">Create detailed PDF reports</p>
              </Button>
              
              <Button 
                variant="default"
                className="flex flex-col items-center justify-center p-6 h-full bg-green-600 hover:bg-green-700"
              >
                <Download className="w-10 h-10 mb-3" />
                <span className="font-semibold">Export Results</span>
                <p className="text-sm text-muted-foreground mt-2">Download data in multiple formats</p>
              </Button>
            </div>
          </div>
        
        </section> */}



        {/* Three Analysis Buttons Section */}
<section className="mb-8">
  <div className="analytics-card p-6">
    <h2 className="text-xl font-semibold text-foreground mb-6">
      Data Analysis Tools
    </h2>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {/* Analysis Selector Button */}
      <div className="flex flex-col items-center justify-center p-6 h-full border rounded-lg bg-gradient-to-br from-blue-50 to-indigo-50">
        <AnalysisSelector
         selectedFileId={selectedFileId}      // ← ADD THIS LINE (MISSING)
         fileName={selectedFileName} 
          onAnalysisSelect={(type) => {
            setSelectedAnalysis(type);
            
            toast({
              title: "Analysis Started",
              description: `Running ${type} analysis...`,
            });
          }}
        />
        <p className="text-sm text-gray-500 mt-4 text-center">
          Choose from summary, trends, or correlation analysis
        </p>
      </div>
      
      

{/* Generate Report Button */}
<Button 
  variant="secondary"
  className="flex flex-col items-center justify-center p-6 h-full bg-purple-600 hover:bg-purple-700 text-white"
  disabled={!selectedAnalysis || !selectedFileId}  // ← ADD THIS
  onClick={async () => {
    if (!selectedAnalysis || !selectedFileId) {
      toast({
        title: "Missing Selection",
        description: !selectedAnalysis 
          ? "Please select an analysis type first" 
          : "Please select a file first",
        variant: "destructive"
      });
      return;
    }

    toast({
      title: "Generating Report",
      description: `Creating ${selectedAnalysis} report for "${selectedFileName}"`,
    });



    
    // TODO: Get fileId from uploaded files - you need to track this
    const fileId = selectedFileId;  // ← CHANGE FROM "some-file-id" TO THIS
    
    if (!fileId) {
      toast({
        title: "No File Selected",
        description: "Please upload a file first",
        variant: "destructive"
      });
      return;
    }
    
    // Show loading
    toast({
      title: "Generating Report",
      description: `Creating ${selectedAnalysis} report...`,
    });
    
    // Call the API
    try {
      const response = await fetch('http://localhost:8000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          file_id: fileId,
          analysis_type: selectedAnalysis
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
      a.download = `${selectedAnalysis}_report.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      toast({
        title: "Report Generated",
        description: `${selectedAnalysis} report downloaded successfully`,
      });
      
    } catch (err: any) {
      console.error('Error generating report:', err);
      toast({
        title: "Generation Failed",
        description: err.message || "Failed to generate report",
        variant: "destructive"
      });
    }
  }}
>
  <FileText className="w-10 h-10 mb-3" />
  <span className="font-semibold">Generate Report</span>
  <p className="text-sm text-white/80 mt-2">
    {!selectedFileId ? "Select a file first" : 
     !selectedAnalysis ? "Select analysis type" : 
     "Create detailed PDF reports"}
  </p>
</Button>
      
      {/* Export Results Button */}
      <Button 
        variant="default"
        className="flex flex-col items-center justify-center p-6 h-full bg-green-600 hover:bg-green-700"
      >
        <Download className="w-10 h-10 mb-3" />
        <span className="font-semibold">Export Results</span>
        <p className="text-sm text-muted-foreground mt-2">Download data in multiple formats</p>
      </Button>
    </div>
    
    {/* Show selected analysis */}
    {selectedAnalysis && (
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="flex items-center justify-between">
          <div>
            <h4 className="font-semibold text-blue-800">
              {selectedAnalysis.charAt(0).toUpperCase() + selectedAnalysis.slice(1)} Analysis Selected
            </h4>
            <p className="text-sm text-blue-600">
              Click "Generate Report" to create a detailed analysis
            </p>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setSelectedAnalysis(null)}
            className="text-blue-600 hover:text-blue-800"
          >
            Clear
          </Button>
        </div>
      </div>
    )}
  </div>
</section>



        {/* Uploaded Files Section */}
        <section>
          <div className="analytics-card p-6">
            <div className="flex items-center gap-2 mb-6">
              <FileSpreadsheet className="w-5 h-5 text-primary" />
              <h2 className="text-lg font-semibold text-foreground">
                Uploaded Files
              </h2>
            </div>
            
            {/* CSVFileCard with refresh trigger */}
            <CSVFileCard 
  refreshTrigger={refreshTrigger}
  onFileSelect={(fileId, fileName) => {
    console.log("File selected:", fileId, fileName);
    setSelectedFileId(fileId);
    setSelectedFileName(fileName || "");
    
    // Optional: Show toast when file is selected
    if (fileId && fileName) {
      toast({
        title: "📁 File Selected",
        description: `"${fileName}" ready for analysis`,
        duration: 2000,
      });
    }
  }}
/>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-card mt-auto">
        <div className="container max-w-6xl mx-auto px-4 py-4">
          <p className="text-sm text-muted-foreground text-center">
            CSV Analytics Dashboard • Frontend Demo
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;