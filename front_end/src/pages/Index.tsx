import { useState } from "react";
import { Database, FileSpreadsheet } from "lucide-react";
import FileUploadZone from "@/components/FileUploadZone";
import CSVFileCard from "@/components/CSVFileCard";
import { CSVFile, mockColumns } from "@/data/mockData";

const Index = () => {
  const [files, setFiles] = useState<CSVFile[]>([]);

  const handleFileUpload = (file: File) => {
    const newFile: CSVFile = {
      id: crypto.randomUUID(),
      name: file.name,
      size: file.size,
      uploadTime: new Date(),
      columns: mockColumns,
      rowCount: Math.floor(Math.random() * 5000) + 500,
    };
    setFiles((prev) => [newFile, ...prev]);
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
          <FileUploadZone onFileUpload={handleFileUpload} />
        </section>

        {/* Uploaded Files Section */}
        <section>
          <div className="flex items-center gap-2 mb-6">
            <FileSpreadsheet className="w-5 h-5 text-primary" />
            <h2 className="text-lg font-semibold text-foreground">
              Uploaded Files
            </h2>
            {files.length > 0 && (
              <span className="ml-2 px-2.5 py-0.5 bg-primary/10 text-primary text-sm font-medium rounded-full">
                {files.length}
              </span>
            )}
          </div>

          {files.length === 0 ? (
            <div className="analytics-card text-center py-12">
              <div className="w-16 h-16 rounded-full bg-secondary flex items-center justify-center mx-auto mb-4">
                <FileSpreadsheet className="w-8 h-8 text-muted-foreground" />
              </div>
              <p className="text-muted-foreground">
                No files uploaded yet. Upload a CSV file to get started.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {files.map((file) => (
                <CSVFileCard key={file.id} file={file} />
              ))}
            </div>
          )}
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
