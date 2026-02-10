import { useState } from "react";
import { BarChart3, TrendingUp, PieChart, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useToast } from "@/hooks/use-toast"; // ← ADD THIS IMPORT

export type AnalysisType = "summary" | "trend" | "correlation" | null;

interface AnalysisSelectorProps {
  selectedFileId?: string;
  fileName?: string;
  onAnalysisSelect?: (type: AnalysisType) => void;
}

const AnalysisSelector = ({
  selectedFileId,
  fileName,
  onAnalysisSelect,
}: AnalysisSelectorProps) => {
  const [selectedType, setSelectedType] = useState<AnalysisType>(null);
  const [open, setOpen] = useState(false);
  const { toast } = useToast(); // ← ADD THIS LINE

  const analysisOptions = [
    {
      id: "summary",
      title: "Summary Statistics",
      description: "Mean, median, min, max, standard deviation",
      icon: BarChart3,
      color: "bg-blue-500",
    },
    {
      id: "trend",
      title: "Trend Analysis",
      description: "Time series patterns and seasonality",
      icon: TrendingUp,
      color: "bg-green-500",
    },
    {
      id: "correlation",
      title: "Correlation Matrix",
      description: "Relationships between numeric columns",
      icon: PieChart,
      color: "bg-purple-500",
    },
  ];

  const handleSelect = (type: AnalysisType) => {
    setSelectedType(type);
    
    // ADD TOAST NOTIFICATION HERE
    if (type === "summary") {
      toast({
        title: "📊 Summary Analysis Started",
        description: fileName 
          ? `Calculating statistics for "${fileName}"`
          : "Calculating summary statistics...",
        duration: 3000,
      });
    } else if (type === "trend") {
      toast({
        title: "📈 Trend Analysis Started",
        description: fileName 
          ? `Analyzing trends in "${fileName}"`
          : "Analyzing time series patterns...",
        duration: 3000,
      });
    } else if (type === "correlation") {
      toast({
        title: "🔗 Correlation Analysis Started",
        description: fileName 
          ? `Finding correlations in "${fileName}"`
          : "Calculating correlation matrix...",
        duration: 3000,
      });
    }
    
    if (onAnalysisSelect) {
      onAnalysisSelect(type);
    }
    setOpen(false);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700">
          <BarChart3 className="w-4 h-4" />
          Select Analysis Type
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5" />
            Select Analysis Type
          </DialogTitle>
          {fileName && (
            <p className="text-sm text-gray-500">
              Analyzing: <span className="font-medium">{fileName}</span>
            </p>
          )}
          {selectedFileId && !fileName && (
            <p className="text-sm text-gray-500">
              File ID: <span className="font-mono text-xs">{selectedFileId.slice(0, 8)}...</span>
            </p>
          )}
        </DialogHeader>

        <div className="space-y-3 py-4">
          {analysisOptions.map((option) => (
            <button
              key={option.id}
              onClick={() => handleSelect(option.id as AnalysisType)}
              className={`w-full flex items-start gap-4 p-4 rounded-lg border transition-all hover:border-primary hover:bg-primary/5 ${
                selectedType === option.id
                  ? "border-primary bg-primary/10"
                  : "border-gray-200"
              }`}
              disabled={!selectedFileId} // Disable if no file selected
            >
              <div
                className={`${option.color} w-10 h-10 rounded-lg flex items-center justify-center ${
                  !selectedFileId ? "opacity-50" : ""
                }`}
              >
                <option.icon className="w-5 h-5 text-white" />
              </div>
              <div className="text-left flex-1">
                <h3 className="font-semibold text-foreground">
                  {option.title}
                </h3>
                <p className="text-sm text-gray-500 mt-1">
                  {option.description}
                </p>
                {!selectedFileId && (
                  <p className="text-xs text-red-500 mt-1">
                    ⚠️ Select a file first
                  </p>
                )}
              </div>
            </button>
          ))}
        </div>

        <div className="flex justify-between items-center pt-4 border-t">
          <div className="text-sm text-gray-500">
            {selectedType ? (
              <span>
                Selected:{" "}
                <span className="font-medium">
                  {analysisOptions.find((opt) => opt.id === selectedType)?.title}
                </span>
                {fileName && (
                  <span className="text-xs ml-2">for "{fileName}"</span>
                )}
              </span>
            ) : (
              "No analysis selected"
            )}
          </div>
          <Button
            variant="outline"
            onClick={() => setOpen(false)}
            className="flex items-center gap-2"
          >
            <X className="w-4 h-4" />
            Close
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default AnalysisSelector;