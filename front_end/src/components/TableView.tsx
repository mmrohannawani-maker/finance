import { useState } from "react";
import { ChevronLeft, ChevronRight, X, Table2 } from "lucide-react";
import { mockTableData, mockColumns } from "@/data/mockData";

interface TableViewProps {
  onClose: () => void;
}

const ROWS_PER_PAGE = 5;

const TableView = ({ onClose }: TableViewProps) => {
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = Math.ceil(mockTableData.length / ROWS_PER_PAGE);

  const startIndex = (currentPage - 1) * ROWS_PER_PAGE;
  const endIndex = startIndex + ROWS_PER_PAGE;
  const currentData = mockTableData.slice(startIndex, endIndex);

  return (
    <div className="animate-fade-in">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
          <Table2 className="w-5 h-5 text-primary" />
          Table View
        </h3>
        <button
          onClick={onClose}
          className="p-1.5 rounded-lg hover:bg-secondary transition-colors"
        >
          <X className="w-4 h-4 text-muted-foreground" />
        </button>
      </div>

      <div className="overflow-x-auto rounded-lg border border-border">
        <table className="table-analytics">
          <thead>
            <tr>
              {mockColumns.map((col) => (
                <th key={col} className="whitespace-nowrap">
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {currentData.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {mockColumns.map((col) => (
                  <td key={col} className="whitespace-nowrap">
                    {typeof row[col] === "number"
                      ? col === "Revenue"
                        ? `$${row[col].toLocaleString()}`
                        : col === "Profit Margin"
                        ? `${row[col]}%`
                        : row[col].toLocaleString()
                      : row[col]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="flex items-center justify-between mt-4">
        <p className="text-sm text-muted-foreground">
          Showing {startIndex + 1}-{Math.min(endIndex, mockTableData.length)} of{" "}
          {mockTableData.length} rows
        </p>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            disabled={currentPage === 1}
            className="p-2 rounded-lg hover:bg-secondary disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="text-sm font-medium px-3">
            {currentPage} / {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
            className="p-2 rounded-lg hover:bg-secondary disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default TableView;
