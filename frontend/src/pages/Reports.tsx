import { useState, useCallback } from "react";
import { generateReport } from "../services/reports";
import { Select } from "../components/ui/Select";
import { ErrorState } from "../components/ui/ErrorState";
import { Badge } from "../components/ui/Badge";
import { FileText, Download, Sparkles, Cpu, CheckCircle2 } from "lucide-react";

export default function ReportsPage() {
  const [reportType, setReportType] = useState("fraud_summary");
  const [format, setFormat] = useState("json");
  const [filters] = useState({});
  const [generating, setGenerating] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const [reportData, setReportData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const reportTypes = [
    { value: "fraud_summary", label: "Executive Fraud Risk Summary (Groq LLM AI)" },
    { value: "model_performance", label: "CatBoost Ensemble Model Evaluation Report" },
    { value: "audit_log", label: "Security & Access Audit Trail Export" },
    { value: "activity_summary", label: "Real-time Streaming Activity Log" },
  ];

  const formats = [
    { value: "json", label: "JSON Data Payload (.json)" },
    { value: "csv", label: "Comma Separated Values (.csv)" },
    { value: "excel", label: "Microsoft Excel Document (.xlsx)" },
    { value: "pdf", label: "Formatted PDF Document (.pdf)" },
  ];

  const handleGenerateReport = useCallback(async () => {
    setGenerating(true);
    setError(null);
    setDownloadUrl(null);
    setReportData(null);

    try {
      const res = await generateReport({
        report_type: reportType,
        format,
        filters,
      });

      setReportData(res);

      if (format === "json") {
        const blob = new Blob([JSON.stringify(res, null, 2)], {
          type: "application/json",
        });
        setDownloadUrl(URL.createObjectURL(blob));
      } else {
        const blob = res instanceof Blob ? res : new Blob([res], { type: format === "csv" ? "text/csv" : "application/octet-stream" });
        setDownloadUrl(URL.createObjectURL(blob));
      }
    } catch (err: any) {
      setError(err.message || "Something went wrong during report generation.");
    } finally {
      setGenerating(false);
    }
  }, [reportType, format, filters]);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }} className="animate-fade-in">
      {/* Subheader Toolbar */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, paddingBottom: 16, borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ width: 36, height: 36, borderRadius: 10, background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.25)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <FileText size={18} color="#818cf8" />
          </div>
          <div>
            <h2 style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9", margin: 0 }}>
              AI Executive Report Generator
            </h2>
            <p style={{ fontSize: 12, color: "#475569", margin: "2px 0 0" }}>
              Synthesize Groq LLM executive threat briefs, model performance metrics, and audit logs
            </p>
          </div>
        </div>

        <Badge variant="indigo" size="md" dot pulse>
          Groq AI Enabled
        </Badge>
      </div>

      <div className="grid-2">
        {/* Left Form Setup */}
        <div className="fs-card" style={{ padding: 24 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 15, fontWeight: 700, color: "#f1f5f9", marginBottom: 20 }}>
            <FileText size={18} color="#818cf8" />
            Report Parameters &amp; Scope
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
            <div>
              <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>
                Report Type &amp; Intelligence Target
              </label>
              <Select
                value={reportType}
                onChange={(e) => setReportType(e.target.value)}
                options={reportTypes}
              />
            </div>

            <div>
              <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>
                Export Target Format
              </label>
              <Select
                value={format}
                onChange={(e) => setFormat(e.target.value)}
                options={formats}
              />
            </div>

            <div style={{ padding: 14, borderRadius: 10, background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)", fontSize: 12, color: "#64748b", lineHeight: 1.6 }}>
              <div style={{ fontWeight: 600, color: "#818cf8", marginBottom: 4, display: "flex", alignItems: "center", gap: 6 }}>
                <Sparkles size={13} /> Groq LLM Integration Active
              </div>
              Executive briefs automatically compile risk metrics, top anomalous merchants, SHAP waterfall vectors, and compliance summaries into auditor-ready reports.
            </div>

            <button
              className="btn-primary"
              disabled={generating}
              onClick={handleGenerateReport}
              style={{ width: "100%", padding: "12px 20px", fontSize: 14, marginTop: 4 }}
            >
              {generating ? (
                <>
                  <span className="animate-spin" style={{ width: 16, height: 16, border: "2px solid rgba(255,255,255,0.3)", borderTopColor: "#fff", borderRadius: "50%", display: "inline-block" }} />
                  Compiling Report Data...
                </>
              ) : (
                <>
                  <Sparkles size={16} />
                  Synthesize Executive Report
                </>
              )}
            </button>
          </div>
        </div>

        {/* Right Output & Download */}
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          <div className="fs-card" style={{ padding: 24, flex: 1, display: "flex", flexDirection: "column", justifyContent: "center" }}>
            {generating ? (
              <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12 }}>
                <div style={{ width: 44, height: 44, borderRadius: 12, background: "rgba(99,102,241,0.15)", border: "1px solid rgba(99,102,241,0.3)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <Cpu size={22} color="#818cf8" className="animate-spin" />
                </div>
                <div style={{ fontSize: 15, fontWeight: 700, color: "#f1f5f9" }}>Groq Llama-3 70B Synthesizing Brief...</div>
                <div style={{ fontSize: 12, color: "#64748b" }}>Extracting transaction features, risk distributions, and anomaly vectors</div>
              </div>
            ) : reportData || downloadUrl ? (
              <div style={{ display: "flex", flexDirection: "column", gap: 16 }} className="animate-fade-in">
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", borderBottom: "1px solid rgba(255,255,255,0.06)", paddingBottom: 12 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                    <div style={{ width: 38, height: 38, borderRadius: 10, background: "rgba(16,185,129,0.15)", border: "1px solid rgba(16,185,129,0.3)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                      <CheckCircle2 size={20} color="#10b981" />
                    </div>
                    <div>
                      <div style={{ fontSize: 15, fontWeight: 700, color: "#f1f5f9" }}>Executive Intelligence Brief</div>
                      <div style={{ fontSize: 11, color: "#64748b" }}>Compiled {new Date().toLocaleTimeString()}</div>
                    </div>
                  </div>
                  {downloadUrl && (
                    <a
                      href={downloadUrl}
                      download={`fraudshield_${reportType}_${Date.now()}.${format}`}
                      className="btn-primary"
                      style={{ textDecoration: "none", padding: "8px 16px", fontSize: 13 }}
                    >
                      <Download size={14} />
                      Export (.{format})
                    </a>
                  )}
                </div>

                {reportData?.summary && (
                  <div style={{ padding: 16, borderRadius: 10, background: "rgba(0,0,0,0.4)", border: "1px solid rgba(255,255,255,0.06)", fontFamily: "monospace", fontSize: 12, color: "#cbd5e1", whiteSpace: "pre-wrap", maxHeight: 240, overflowY: "auto", textAlign: "left" }}>
                    {reportData.summary}
                  </div>
                )}

                {reportData?.recommendations && (
                  <div style={{ padding: 12, borderRadius: 8, background: "rgba(99,102,241,0.08)", border: "1px solid rgba(99,102,241,0.2)", fontSize: 12, color: "#a5b4fc", textAlign: "left" }}>
                    <strong>Groq Recommendation:</strong> {reportData.recommendations}
                  </div>
                )}
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10, color: "#475569" }}>
                <FileText size={40} style={{ opacity: 0.3 }} />
                <div style={{ fontSize: 14, fontWeight: 600, color: "#64748b" }}>No Report Generated Yet</div>
                <div style={{ fontSize: 12 }}>Select options on the left and click "Synthesize Executive Report"</div>
              </div>
            )}
          </div>

          {error && (
            <ErrorState
              title="Report Synthesis Failed"
              message={error}
              onRetry={handleGenerateReport}
            />
          )}
        </div>
      </div>
    </div>
  );
}