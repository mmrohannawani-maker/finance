import { useState, useEffect } from "react";
import { ChevronLeft, ChevronRight, X, Table2, ArrowLeft } from "lucide-react";
import { getFileData } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';
import { useParams, useNavigate } from "react-router-dom";

const TableView = () => {
  const { fileId } = useParams<{ fileId: string }>();
  const navigate = useNavigate();
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [columns, setColumns] = useState<string[]>([]);
  const [data, setData] = useState<any[]>([]);
  const [totalRows, setTotalRows] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const { toast } = useToast();

  useEffect(() => {
    if (fileId) {
      fetchTableData();
    }
  }, [fileId, currentPage, rowsPerPage]);

  const fetchTableData = async () => {
    try {
      setLoading(true);
      const response = await getFileData(fileId!, currentPage, rowsPerPage);
      
      setData(response.data.data || []);
      setColumns(response.data.file.columns || []);
      setTotalRows(response.data.pagination.total || 0);
    } catch (error) {
      console.error('Failed to load table data:', error);
      toast({ 
        title: 'Error', 
        description: 'Failed to load table data from backend' 
      });
    } finally {
      setLoading(false);
    }
  };

  const totalPages = Math.ceil(totalRows / rowsPerPage);
  const startIndex = (currentPage - 1) * rowsPerPage + 1;
  const endIndex = Math.min(currentPage * rowsPerPage, totalRows);

  const formatCellValue = (value: any, columnName: string): string => {
    if (value === null || value === undefined) return '—';
    
    if (typeof value === 'number') {
      if (columnName.toLowerCase().includes('price') || 
          columnName.toLowerCase().includes('amount') || 
          columnName.toLowerCase().includes('revenue') ||
          columnName.toLowerCase().includes('cost')) {
        return `$${value.toLocaleString()}`;
      }
      else if (columnName.toLowerCase().includes('percent') || 
               columnName.toLowerCase().includes('margin') ||
               columnName.toLowerCase().includes('rate')) {
        return `${value}%`;
      }
      else {
        return value.toLocaleString();
      }
    }
    
    return String(value);
  };

  if (loading) {
    return (
      <div className="animate-fade-in p-6">
        <div className="flex items-center gap-4 mb-6">
          <button
            onClick={() => navigate(-1)}
            className="p-1.5 rounded-lg hover:bg-secondary transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
            <Table2 className="w-5 h-5 text-primary" />
            Loading Table Data...
          </h3>
        </div>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="animate-fade-in p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate(-1)}
            className="p-1.5 rounded-lg hover:bg-secondary transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
            <Table2 className="w-5 h-5 text-primary" />
            Table View
          </h3>
        </div>
      </div>

      {columns.length === 0 || data.length === 0 ? (
        <div className="text-center py-8 border border-border rounded-lg">
          <p className="text-muted-foreground">No data available for this file</p>
        </div>
      ) : (
        <>
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="table-analytics">
              <thead>
                <tr>
                  <th className="whitespace-nowrap">#</th>
                  {columns.map((col) => (
                    <th key={col} className="whitespace-nowrap">
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    <td className="whitespace-nowrap font-medium">
                      {startIndex + rowIndex}
                    </td>
                    {columns.map((col) => (
                      <td key={col} className="whitespace-nowrap">
                        {formatCellValue(row[col], col)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="flex items-center justify-between mt-4">
            <div className="flex items-center gap-4">
              <p className="text-sm text-muted-foreground">
                Showing {startIndex}-{endIndex} of {totalRows.toLocaleString()} rows
              </p>
              <select 
                value={rowsPerPage}
                onChange={(e) => {
                  setRowsPerPage(Number(e.target.value));
                  setCurrentPage(1);
                }}
                className="text-sm border border-border rounded px-2 py-1 bg-background"
              >
                <option value="5">5 rows</option>
                <option value="10">10 rows</option>
                <option value="20">20 rows</option>
                <option value="50">50 rows</option>
              </select>
            </div>
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
        </>
      )}
    </div>
  );
};

export default TableView;