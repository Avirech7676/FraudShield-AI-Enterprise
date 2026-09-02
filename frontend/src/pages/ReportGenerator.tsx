import { useState, useEffect } from "react";
import { getReportHistory, generateReport, type ReportRequest } from "../services/reportService";

export default function ReportGeneratorPage() {
  const [reportType, setReportType] = useState("fraud_summary");
  const [format, setFormat] = useState("JSON");
  const [filters, setFilters] = useState({});
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [preview, setPreview] = useState<any>(null);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const data = await getReportHistory();
        if (mounted) setHistory(data);
      } catch (err) {
        if (mounted) setError("Failed to load report history");
      }
    })();
    return () => {
      mounted = false;
    };
  }, []);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    setPreview(null);
    try {
      const request: ReportRequest = {
        report_type: reportType,
        format: format,
        filters: filters,
      };
      const data = await generateReport(request);

      const text = await data.text();
      try {
        const json = JSON.parse(text);
        setPreview(json);
      } catch (e) {
        const url = window.URL.createObjectURL(data);
        const a = document.createElement("a");
        const fileName = `report_${reportType}_${new Date().toISOString()}.${format.toLowerCase()}`;
        a.href = url;
        a.download = fileName;
        a.click();
        window.URL.revokeObjectURL(url);
      }
    } catch (err: any) {
      setError(err.message || "Failed to generate report");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <h1>Report Generator</h1>
      <div className="report-generator">
        <div className="form-group">
          <label>Report Type:</label>
          <select
            value={reportType}
            onChange={(e) => setReportType(e.target.value)}
          >
            <option value="fraud_summary">Fraud Summary</option>
            <option value="model_performance">Model Performance</option>
            <option value="audit_log">Audit Log</option>
            <option value="activity_summary">Activity Summary</option>
          </select>
        </div>

        <div className="form-group">
          <label>Format:</label>
          <select
            value={format}
            onChange={(e) => setFormat(e.target.value)}
          >
            <option value="JSON">JSON</option>
            <option value="CSV">CSV</option>
            <option value="EXCEL">Excel</option>
            <option value="PDF">PDF</option>
          </select>
        </div>

        <div className="form-group">
          <label>Filters (JSON):</label>
          <textarea
            value={JSON.stringify(filters, null, 2)}
            onChange={(e) => {
              try {
                setFilters(JSON.parse(e.target.value));
              } catch (err) {
                // Ignore invalid JSON
              }
            }}
            rows={4}
            placeholder='{"dateFrom": "2024-01-01", "dateTo": "2024-12-31"}'
          />
        </div>

        <button onClick={handleGenerate} disabled={loading}>
          {loading ? "Generating..." : "Generate Report"}
        </button>

        {error && <div className="error">{error}</div>}
        {preview && (
          <div className="preview">
            <h3>Preview:</h3>
            <pre>{JSON.stringify(preview, null, 2)}</pre>
          </div>
        )}
      </div>

      <h2>Report History</h2>
      {history.length === 0 ? (
        <p>No reports generated yet.</p>
      ) : (
        <ul>
          {history.map((report, index) => (
            <li key={index}>
              <strong>{report.report_type}</strong> - {new Date(
                report.created_at
              ).toLocaleString()}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}