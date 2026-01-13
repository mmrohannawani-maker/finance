import { useState, useEffect } from "react";
import { FileSpreadsheet, Clock, HardDrive, Sparkles, BarChart3, Eye, Trash2 } from "lucide-react";
import { getFiles, deleteFile } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';
import SummaryPanel from "./SummaryPanel";
import ChartBuilder from "./ChartBuilder";

type ViewMode = "none" | "summary" | "chart";

interface BackendFile {
  id: string;
  original_name: string;
  file_size: number;
  row_count: number;
  column_count: number;
  columns: string[];
  created_at: string;
  filename?: string;
}

const CSVFileCard = () => {
  const [viewMode, setViewMode] = useState<ViewMode>("none");
  const [selectedFileId, setSelectedFileId] = useState<string | null>(null);
  const [files, setFiles] = useState<BackendFile[]>([]);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const response = await getFiles();
      setFiles(response.data || []);
    } catch (error) {
      console.error('Failed to load files:', error);
      toast({ 
        title: 'Error', 
        description: 'Failed to load files from backend' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (fileId: string, fileName: string) => {
    if (!confirm(`Delete "${fileName}"?`)) return;
    
    try {
      await deleteFile(fileId);
      toast({ title: 'Success', description: 'File deleted' });
      fetchFiles(); // Refresh list
    } catch (error) {
      console.error('Delete failed:', error);
      toast({ title: 'Error', description: 'Failed to delete file' });
    }
  };

  const handleButtonClick = (mode: ViewMode, fileId: string) => {
    setSelectedFileId(fileId);
    setViewMode(viewMode === mode ? "none" : mode);
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatTime = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (loading) {
    return (
      <div className="analytics-card animate-fade-in">
        <div className="flex justify-center items-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  if (files.length === 0) {
    return (
      <div className="analytics-card animate-fade-in text-center py-8">
        <FileSpreadsheet className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="font-semibold text-foreground mb-2">No files uploaded</h3>
        <p className="text-muted-foreground">Upload a CSV file to get started</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {files.map((file) => (
        <div key={file.id} className="analytics-card animate-fade-in">
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-start gap-4 flex-1">
              <div className="w-12 h-12 rounded-lg gradient-header flex items-center justify-center flex-shrink-0">
                <FileSpreadsheet className="w-6 h-6 text-primary-foreground" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold text-foreground truncate">
                    {file.original_name}
                  </h3>
                  <div className="flex gap-1">
                    <button
                      onClick={() => window.open(`/table/${file.id}`, '_blank')}
                      className="p-1 hover:bg-gray-100 rounded"
                      title="Open full table view"
                    >
                      <Eye className="w-4 h-4 text-gray-600" />
                    </button>
                    <button
                      onClick={() => handleDelete(file.id, file.original_name)}
                      className="p-1 hover:bg-red-50 rounded"
                      title="Delete file"
                    >
                      <Trash2 className="w-4 h-4 text-red-500" />
                    </button>
                  </div>
                </div>
                <div className="flex items-center gap-4 mt-1 text-sm text-muted-foreground">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" />
                    {formatTime(file.created_at)}
                  </span>
                  <span className="flex items-center gap-1">
                    <HardDrive className="w-3.5 h-3.5" />
                    {formatFileSize(file.file_size)}
                  </span>
                  <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                    {file.row_count} rows × {file.column_count} cols
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap gap-2 mb-4">
            <button
              onClick={() => handleButtonClick("summary", file.id)}
              className={`btn-analytics ${
                viewMode === "summary" && selectedFileId === file.id
                  ? "bg-primary text-primary-foreground"
                  : "btn-analytics-ghost"
              }`}
            >
              <Sparkles className="w-4 h-4" />
              Summary
            </button>
            <button
              onClick={() => handleButtonClick("chart", file.id)}
              className={`btn-analytics ${
                viewMode === "chart" && selectedFileId === file.id
                  ? "bg-primary text-primary-foreground"
                  : "btn-analytics-ghost"
              }`}
            >
              <BarChart3 className="w-4 h-4" />
              Charts
            </button>
          </div>

          {viewMode !== "none" && selectedFileId === file.id && (
            <div className="pt-4 border-t border-border">
              {viewMode === "summary" && (
                <SummaryPanel 
                  fileName={file.original_name} 
                  onClose={() => setViewMode("none")} 
                />
              )}
              {viewMode === "chart" && (
                <ChartBuilder 
                  onClose={() => setViewMode("none")} 
                />
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default CSVFileCard;