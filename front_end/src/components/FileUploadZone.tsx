import { useState, useCallback } from "react";
import { Upload, FileSpreadsheet } from "lucide-react";
import { uploadFile } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

const FileUploadZone = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const { toast } = useToast();

  const handleFileUpload = async (file: File) => {
    // Strict CSV validation
    if (!file.name.toLowerCase().endsWith('.csv')) {
      toast({ 
        title: 'Invalid File Type', 
        description: 'Only CSV files are allowed.',
        variant: 'destructive'
      });
      return;
    }

    if (file.size > 50 * 1024 * 1024) { // 50MB
      toast({ 
        title: 'File Too Large', 
        description: 'File must be under 50MB.',
        variant: 'destructive'
      });
      return;
    }

    setUploading(true);
    try {
      await uploadFile(file);
      toast({ 
        title: 'Success!', 
        description: 'File uploaded successfully.' 
      });
      
      // Refresh after 1 second
      setTimeout(() => {
        window.location.reload();
      }, 1000);
      
    } catch (error: any) {
      console.error('Upload error:', error);
      toast({ 
        title: 'Upload Failed', 
        description: error.response?.data?.detail || 'Please try again.',
        variant: 'destructive'
      });
    } finally {
      setUploading(false);
    }
  };

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDragIn = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragOut = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);

      const files = e.dataTransfer.files;
      if (files && files.length > 0) {
        handleFileUpload(files[0]);
      }
    },
    []
  );

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileUpload(files[0]);
    }
    e.target.value = "";
  };

  return (
    <div
      className={`upload-zone text-center ${isDragging ? "upload-zone-active" : ""} ${uploading ? "opacity-50 cursor-not-allowed" : ""}`}
      onDragEnter={handleDragIn}
      onDragLeave={handleDragOut}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input
        type="file"
        accept=".csv"
        onChange={handleFileInput}
        disabled={uploading}
        className="hidden"
        id="file-upload"
      />
      <label htmlFor="file-upload" className={`cursor-pointer ${uploading ? "cursor-not-allowed" : ""}`}>
        <div className="flex flex-col items-center gap-4">
          <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
            {uploading ? (
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            ) : isDragging ? (
              <FileSpreadsheet className="w-8 h-8 text-primary" />
            ) : (
              <Upload className="w-8 h-8 text-primary" />
            )}
          </div>
          <div>
            <p className="text-lg font-semibold text-foreground">
              {uploading ? 'Uploading...' : 'Upload CSV File'}
            </p>
            <p className="text-sm text-muted-foreground mt-1">
              Drag and drop or click to browse
            </p>
            <p className="text-xs text-gray-400 mt-2">
              Only .csv files • Max 2000MB
            </p>
          </div>
          <button
            type="button"
            disabled={uploading}
            className={`btn-analytics-secondary ${uploading ? "opacity-50 cursor-not-allowed" : ""}`}
          >
            {uploading ? 'Processing...' : 'Select CSV File'}
          </button>
        </div>
      </label>
    </div>
  );
};

export default FileUploadZone;