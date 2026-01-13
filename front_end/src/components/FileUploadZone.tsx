import { useState, useCallback } from "react";
import { Upload, FileSpreadsheet } from "lucide-react";
import { uploadFile } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

interface FileUploadZoneProps {
  onFileUpload?: (file: File) => void;
}

const FileUploadZone = ({ onFileUpload }: FileUploadZoneProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const { toast } = useToast();

  const handleFileUpload = async (file: File) => {
    try {
      await uploadFile(file);
      toast({ 
        title: 'Success', 
        description: 'File uploaded successfully!' 
      });
      
      // Call parent callback if provided
      if (onFileUpload) {
        onFileUpload(file);
      }
      
      // Trigger page refresh after 1 second
      setTimeout(() => {
        window.location.reload();
      }, 1000);
      
    } catch (error) {
      toast({ 
        title: 'Error', 
        description: 'Upload failed. Please try again.' 
      });
      console.error('Upload error:', error);
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
        const file = files[0];
        if (file.name.toLowerCase().endsWith(".csv")) {
          handleFileUpload(file);
        } else {
          toast({ 
            title: 'Invalid File', 
            description: 'Please upload a CSV file only.' 
          });
        }
      }
    },
    [toast]
  );

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (file.name.toLowerCase().endsWith(".csv")) {
        handleFileUpload(file);
      } else {
        toast({ 
          title: 'Invalid File', 
          description: 'Please upload a CSV file only.' 
        });
      }
    }
    e.target.value = "";
  };

  return (
    <div
      className={`upload-zone text-center ${isDragging ? "upload-zone-active" : ""}`}
      onDragEnter={handleDragIn}
      onDragLeave={handleDragOut}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input
        type="file"
        accept=".csv"
        onChange={handleFileInput}
        className="hidden"
        id="file-upload"
      />
      <label htmlFor="file-upload" className="cursor-pointer">
        <div className="flex flex-col items-center gap-4">
          <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
            {isDragging ? (
              <FileSpreadsheet className="w-8 h-8 text-primary" />
            ) : (
              <Upload className="w-8 h-8 text-primary" />
            )}
          </div>
          <div>
            <p className="text-lg font-semibold text-foreground">
              Upload your CSV file
            </p>
            <p className="text-sm text-muted-foreground mt-1">
              Drag and drop or click to browse
            </p>
          </div>
          <span className="btn-analytics-secondary">
            Select CSV File
          </span>
        </div>
      </label>
    </div>
  );
};

export default FileUploadZone;