import { X, TrendingUp, Database, Columns, Sparkles } from "lucide-react";
import { generateMockSummary } from "@/data/mockData";

interface SummaryPanelProps {
  fileName: string;
  onClose: () => void;
}

const SummaryPanel = ({ fileName, onClose }: SummaryPanelProps) => {
  const summary = generateMockSummary(fileName);

  return (
    <div className="animate-fade-in">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-primary" />
          Data Summary
        </h3>
        <button
          onClick={onClose}
          className="p-1.5 rounded-lg hover:bg-secondary transition-colors"
        >
          <X className="w-4 h-4 text-muted-foreground" />
        </button>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="stat-card">
          <div className="flex items-center gap-2 text-muted-foreground mb-1">
            <Database className="w-4 h-4" />
            <span className="text-xs font-medium">Rows</span>
          </div>
          <p className="text-2xl font-bold text-foreground">
            {summary.rowCount.toLocaleString()}
          </p>
        </div>
        <div className="stat-card">
          <div className="flex items-center gap-2 text-muted-foreground mb-1">
            <Columns className="w-4 h-4" />
            <span className="text-xs font-medium">Columns</span>
          </div>
          <p className="text-2xl font-bold text-foreground">
            {summary.columnCount}
          </p>
        </div>
      </div>

      <div className="mb-6">
        <h4 className="text-sm font-medium text-muted-foreground mb-3">
          Column Names
        </h4>
        <div className="flex flex-wrap gap-2">
          {summary.columns.map((col) => (
            <span
              key={col}
              className="px-3 py-1 bg-secondary text-secondary-foreground text-xs font-medium rounded-full"
            >
              {col}
            </span>
          ))}
        </div>
      </div>

      <div className="mb-6">
        <h4 className="text-sm font-medium text-muted-foreground mb-3">
          Key Metrics
        </h4>
        <div className="space-y-3">
          {summary.insights.map((insight, index) => (
            <div
              key={index}
              className="flex justify-between items-center py-2 border-b border-border last:border-0"
            >
              <span className="text-sm text-muted-foreground">
                {insight.label}
              </span>
              <span className="text-sm font-semibold text-foreground">
                {insight.value}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h4 className="text-sm font-medium text-muted-foreground mb-3 flex items-center gap-2">
          <TrendingUp className="w-4 h-4" />
          Trends & Insights
        </h4>
        <ul className="space-y-2">
          {summary.trends.map((trend, index) => (
            <li
              key={index}
              className="flex items-start gap-2 text-sm text-foreground"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 flex-shrink-0" />
              {trend}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default SummaryPanel;
