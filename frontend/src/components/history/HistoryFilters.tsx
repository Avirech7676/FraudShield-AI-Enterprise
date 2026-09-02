type HistoryFiltersType = {
  customerId: string;
  transactionId: string;
  dateFrom: string;
  dateTo: string;
  amountMin: string;
  amountMax: string;
  riskLevel: string;
  merchant: string;
  status: string;
};

type Props = {
  filters: HistoryFiltersType;
  setFilters: React.Dispatch<React.SetStateAction<HistoryFiltersType>>;
};

export default function HistoryFilters({ filters, setFilters }: Props) {
  const handleChange = (field: keyof HistoryFiltersType, value: string) => {
    setFilters((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <div className="filters-bar">
      <div className="filter-group">
        <label>Transaction ID</label>
        <input
          type="text"
          value={filters.transactionId}
          onChange={(e) => handleChange("transactionId", e.target.value)}
          placeholder="Search by ID"
        />
      </div>

      <div className="filter-group">
        <label>Customer ID</label>
        <input
          type="text"
          value={filters.customerId}
          onChange={(e) => handleChange("customerId", e.target.value)}
          placeholder="Search customer"
        />
      </div>

      <div className="filter-group">
        <label>Date From</label>
        <input
          type="date"
          value={filters.dateFrom}
          onChange={(e) => handleChange("dateFrom", e.target.value)}
        />
      </div>

      <div className="filter-group">
        <label>Date To</label>
        <input
          type="date"
          value={filters.dateTo}
          onChange={(e) => handleChange("dateTo", e.target.value)}
        />
      </div>

      <div className="filter-group">
        <label>Risk Level</label>
        <select
          value={filters.riskLevel}
          onChange={(e) => handleChange("riskLevel", e.target.value)}
        >
          <option value="">All</option>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>
      </div>

      <div className="filter-group">
        <label>Status</label>
        <select
          value={filters.status}
          onChange={(e) => handleChange("status", e.target.value)}
        >
          <option value="">All</option>
          <option value="Fraud">Fraud</option>
          <option value="Legitimate">Legitimate</option>
        </select>
      </div>
    </div>
  );
}