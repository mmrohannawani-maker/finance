import { useState } from "react";
import { FileSpreadsheet, Clock, HardDrive, Sparkles, Table2, BarChart3 } from "lucide-react";
import { CSVFile, formatFileSize, formatTime } from "@/data/mockData";
import SummaryPanel from "./SummaryPanel";
import TableView from "./TableView";
import ChartBuilder from "./ChartBuilder";

interface CSVFileCardProps {
  file: CSVFile;
}

type ViewMode = "none" | "summary" | "table" | "chart";

const CSVFileCard = ({ file }: CSVFileCardProps) => {
  const [viewMode, setViewMode] = useState<ViewMode>("none");

  const handleButtonClick = (mode: ViewMode) => {
    setViewMode(viewMode === mode ? "none" : mode);
  };

  return (
    <div className="analytics-card animate-fade-in">
      <div className="flex items-start gap-4 mb-4">
        <div className="w-12 h-12 rounded-lg gradient-header flex items-center justify-center flex-shrink-0">
          <FileSpreadsheet className="w-6 h-6 text-primary-foreground" />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-foreground truncate">{file.name}</h3>
          <div className="flex items-center gap-4 mt-1 text-sm text-muted-foreground">
            <span className="flex items-center gap-1">
              <Clock className="w-3.5 h-3.5" />
              {formatTime(file.uploadTime)}
            </span>
            <span className="flex items-center gap-1">
              <HardDrive className="w-3.5 h-3.5" />
              {formatFileSize(file.size)}
            </span>
          </div>
        </div>
      </div>

      <div className="flex flex-wrap gap-2 mb-4">
        <button
          onClick={() => handleButtonClick("summary")}
          className={`btn-analytics ${
            viewMode === "summary"
              ? "bg-primary text-primary-foreground"
              : "btn-analytics-ghost"
          }`}
        >
          <Sparkles className="w-4 h-4" />
          Summary
        </button>
        <button
          onClick={() => handleButtonClick("table")}
          className={`btn-analytics ${
            viewMode === "table"
              ? "bg-primary text-primary-foreground"
              : "btn-analytics-ghost"
          }`}
        >
          <Table2 className="w-4 h-4" />
          Table View
        </button>
        <button
          onClick={() => handleButtonClick("chart")}
          className={`btn-analytics ${
            viewMode === "chart"
              ? "bg-primary text-primary-foreground"
              : "btn-analytics-ghost"
          }`}
        >
          <BarChart3 className="w-4 h-4" />
          Charts
        </button>
      </div>

      {viewMode !== "none" && (
        <div className="pt-4 border-t border-border">
          {viewMode === "summary" && (
            <SummaryPanel fileName={file.name} onClose={() => setViewMode("none")} />
          )}
          {viewMode === "table" && <TableView onClose={() => setViewMode("none")} />}
          {viewMode === "chart" && <ChartBuilder onClose={() => setViewMode("none")} />}
        </div>
      )}
    </div>
  );
};

export default CSVFileCard;
