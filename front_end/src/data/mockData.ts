export interface CSVFile {
  id: string;
  name: string;
  size: number;
  uploadTime: Date;
  columns: string[];
  rowCount: number;
}

export interface MockTableRow {
  [key: string]: string | number;
}

export const mockColumns = [
  "Product", "Category", "Revenue", "Units Sold", "Region", "Date", "Customer ID", "Profit Margin"
];

export const mockTableData: MockTableRow[] = [
  { Product: "Widget A", Category: "Electronics", Revenue: 12500, "Units Sold": 250, Region: "North", Date: "2024-01-15", "Customer ID": "C001", "Profit Margin": 22.5 },
  { Product: "Widget B", Category: "Electronics", Revenue: 8900, "Units Sold": 178, Region: "South", Date: "2024-01-16", "Customer ID": "C002", "Profit Margin": 18.3 },
  { Product: "Gadget X", Category: "Accessories", Revenue: 15600, "Units Sold": 312, Region: "East", Date: "2024-01-17", "Customer ID": "C003", "Profit Margin": 28.7 },
  { Product: "Gadget Y", Category: "Accessories", Revenue: 9200, "Units Sold": 184, Region: "West", Date: "2024-01-18", "Customer ID": "C004", "Profit Margin": 21.1 },
  { Product: "Device Z", Category: "Hardware", Revenue: 22400, "Units Sold": 448, Region: "North", Date: "2024-01-19", "Customer ID": "C005", "Profit Margin": 32.4 },
  { Product: "Tool Alpha", Category: "Tools", Revenue: 6700, "Units Sold": 134, Region: "South", Date: "2024-01-20", "Customer ID": "C006", "Profit Margin": 15.8 },
  { Product: "Tool Beta", Category: "Tools", Revenue: 11200, "Units Sold": 224, Region: "East", Date: "2024-01-21", "Customer ID": "C007", "Profit Margin": 24.6 },
  { Product: "Component M", Category: "Hardware", Revenue: 18900, "Units Sold": 378, Region: "West", Date: "2024-01-22", "Customer ID": "C008", "Profit Margin": 29.2 },
  { Product: "Component N", Category: "Hardware", Revenue: 14300, "Units Sold": 286, Region: "North", Date: "2024-01-23", "Customer ID": "C009", "Profit Margin": 26.1 },
  { Product: "Part Q", Category: "Electronics", Revenue: 7800, "Units Sold": 156, Region: "South", Date: "2024-01-24", "Customer ID": "C010", "Profit Margin": 19.5 },
  { Product: "Part R", Category: "Electronics", Revenue: 20100, "Units Sold": 402, Region: "East", Date: "2024-01-25", "Customer ID": "C011", "Profit Margin": 31.2 },
  { Product: "Module S", Category: "Accessories", Revenue: 13500, "Units Sold": 270, Region: "West", Date: "2024-01-26", "Customer ID": "C012", "Profit Margin": 25.8 },
];

export const generateMockChartData = (chartType: string) => {
  if (chartType === "Pie") {
    return [
      { name: "Electronics", value: 35, fill: "hsl(217, 91%, 60%)" },
      { name: "Accessories", value: 28, fill: "hsl(142, 76%, 36%)" },
      { name: "Hardware", value: 25, fill: "hsl(38, 92%, 50%)" },
      { name: "Tools", value: 12, fill: "hsl(280, 65%, 60%)" },
    ];
  }

  return [
    { name: "Jan", value: 4000, value2: 2400 },
    { name: "Feb", value: 3000, value2: 1398 },
    { name: "Mar", value: 5000, value2: 3800 },
    { name: "Apr", value: 2780, value2: 3908 },
    { name: "May", value: 1890, value2: 4800 },
    { name: "Jun", value: 6390, value2: 3800 },
    { name: "Jul", value: 3490, value2: 4300 },
  ];
};

export const generateMockSummary = (fileName: string) => ({
  rowCount: Math.floor(Math.random() * 5000) + 500,
  columnCount: Math.floor(Math.random() * 12) + 5,
  columns: mockColumns.slice(0, Math.floor(Math.random() * 4) + 4),
  insights: [
    { label: "Average Revenue", value: `$${(Math.random() * 20000 + 5000).toFixed(2)}` },
    { label: "Total Units Sold", value: (Math.floor(Math.random() * 10000) + 1000).toLocaleString() },
    { label: "Top Region", value: ["North", "South", "East", "West"][Math.floor(Math.random() * 4)] },
    { label: "Data Quality", value: `${Math.floor(Math.random() * 10) + 90}%` },
  ],
  trends: [
    "Revenue trending upward by 12% month-over-month",
    "North region shows highest growth potential",
    "Electronics category dominates with 35% market share",
  ],
});

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};

export const formatTime = (date: Date): string => {
  return date.toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};
