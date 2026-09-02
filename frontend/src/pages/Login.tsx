import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ShieldAlert, User, Lock, ArrowRight, ShieldCheck, Activity, Cpu, Eye, EyeOff, Zap } from "lucide-react";

import { login } from "../services/auth";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const navigate = useNavigate();
  const { login: authLogin } = useAuth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const result = await login({ username, password });
      authLogin(result.access_token, username, result.role);
      navigate("/dashboard", { replace: true });
    } catch (err: any) {
      const serverDetail = err.response?.data?.detail;
      const errorMsg = serverDetail ? `${serverDetail}. (Default credentials: admin / admin123)` : (err.message || "Invalid credentials. Please try again.");
      setMessage(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const features = [
    { icon: ShieldCheck, color: "#10b981", label: "Sub-100ms Inference", desc: "Real-time fraud detection at scale" },
    { icon: Activity,    color: "#6366f1", label: "Live Transaction Streams", desc: "Continuous behavioral pattern analysis" },
    { icon: Cpu,         color: "#a78bfa", label: "Groq LLM Reports",       desc: "AI-generated executive risk briefs" },
    { icon: Zap,         color: "#f59e0b", label: "SHAP Explainability",     desc: "Transparent, auditable decisions" },
  ];

  return (
    <div className="login-bg min-h-screen flex items-center justify-center p-4 md:p-8">
      {/* Decorative orbs */}
      <div style={{ position: "absolute", top: "10%", left: "5%", width: 400, height: 400, borderRadius: "50%", background: "radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%)", pointerEvents: "none" }} />
      <div style={{ position: "absolute", bottom: "10%", right: "5%", width: 300, height: 300, borderRadius: "50%", background: "radial-gradient(circle, rgba(168,85,247,0.10) 0%, transparent 70%)", pointerEvents: "none" }} />

      <div style={{ width: "100%", maxWidth: 980, display: "grid", gridTemplateColumns: "5fr 7fr", background: "rgba(255,255,255,0.025)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 20, overflow: "hidden", boxShadow: "0 32px 80px rgba(0,0,0,0.7)", backdropFilter: "blur(20px)", position: "relative", zIndex: 10 }}>
        {/* ── Left Hero Panel ── */}
        <div style={{ padding: "44px 36px", background: "linear-gradient(160deg, rgba(99,102,241,0.12) 0%, rgba(2,4,10,0.5) 100%)", borderRight: "1px solid rgba(255,255,255,0.06)", display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
          {/* Brand */}
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 32 }}>
              <div style={{ width: 44, height: 44, borderRadius: 12, background: "linear-gradient(135deg, #6366f1, #4f46e5)", display: "flex", alignItems: "center", justifyContent: "center", boxShadow: "0 0 24px rgba(99,102,241,0.4)", border: "1px solid rgba(99,102,241,0.4)", flexShrink: 0 }}>
                <ShieldAlert size={22} color="#fff" />
              </div>
              <div>
                <div style={{ fontSize: 18, fontWeight: 800, color: "#f1f5f9", letterSpacing: "-0.02em", lineHeight: 1 }}>FraudShield</div>
                <div style={{ fontSize: 10, fontWeight: 600, color: "#818cf8", letterSpacing: "0.15em", textTransform: "uppercase", marginTop: 3 }}>Enterprise AI</div>
              </div>
            </div>

            <h1 style={{ fontSize: 26, fontWeight: 800, color: "#f1f5f9", letterSpacing: "-0.03em", lineHeight: 1.2, marginBottom: 12 }}>
              Real-Time AI<br />
              <span className="gradient-text">Threat Intelligence</span>
            </h1>
            <p style={{ fontSize: 13, color: "#64748b", lineHeight: 1.7, marginBottom: 28 }}>
              Enterprise-grade fraud detection powered by CatBoost ensemble models, SHAP explainability, and Groq LLM reporting.
            </p>

            {/* Feature list */}
            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {features.map(({ icon: Icon, color, label, desc }) => (
                <div key={label} style={{ display: "flex", alignItems: "center", gap: 12, padding: "11px 14px", borderRadius: 10, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }}>
                  <div style={{ width: 34, height: 34, borderRadius: 8, background: `${color}18`, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                    <Icon size={16} color={color} />
                  </div>
                  <div>
                    <div style={{ fontSize: 12, fontWeight: 600, color: "#e2e8f0", lineHeight: 1.2 }}>{label}</div>
                    <div style={{ fontSize: 11, color: "#475569", marginTop: 2 }}>{desc}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Footer */}
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", paddingTop: 24, marginTop: 24, borderTop: "1px solid rgba(255,255,255,0.05)", fontSize: 11, color: "#334155" }}>
            <span>PCI-DSS • SOC 2 Type II</span>
            <span style={{ color: "#818cf8" }}>v2.0 Enterprise</span>
          </div>
        </div>

        {/* ── Right Form Panel ── */}
        <div style={{ padding: "52px 44px", display: "flex", flexDirection: "column", justifyContent: "center" }}>
          {/* Live status */}
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 32 }}>
            <span className="status-dot online" />
            <span style={{ fontSize: 12, color: "#10b981", fontWeight: 500 }}>All systems operational</span>
          </div>

          <div style={{ marginBottom: 32 }}>
            <h2 style={{ fontSize: 24, fontWeight: 800, color: "#f1f5f9", letterSpacing: "-0.03em", marginBottom: 6 }}>
              Sign In to Terminal
            </h2>
            <p style={{ fontSize: 13, color: "#475569" }}>
              Enter your credentials to access the fraud operations portal.
            </p>
          </div>

          <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 18 }}>
            {/* Username */}
            <div>
              <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", letterSpacing: "0.04em", textTransform: "uppercase", marginBottom: 8 }}>Username</label>
              <div style={{ position: "relative" }}>
                <User size={15} color="#475569" style={{ position: "absolute", left: 13, top: "50%", transform: "translateY(-50%)", pointerEvents: "none" }} />
                <input
                  id="username"
                  type="text"
                  className="fs-input"
                  style={{ paddingLeft: 38 }}
                  placeholder="Enter your operational username"
                  value={username}
                  onChange={e => setUsername(e.target.value)}
                  autoFocus
                  required
                  autoComplete="username"
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", letterSpacing: "0.04em", textTransform: "uppercase", marginBottom: 8 }}>Password</label>
              <div style={{ position: "relative" }}>
                <Lock size={15} color="#475569" style={{ position: "absolute", left: 13, top: "50%", transform: "translateY(-50%)", pointerEvents: "none" }} />
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  className="fs-input"
                  style={{ paddingLeft: 38, paddingRight: 44 }}
                  placeholder="Enter your security password"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  required
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(p => !p)}
                  style={{ position: "absolute", right: 13, top: "50%", transform: "translateY(-50%)", background: "none", border: "none", cursor: "pointer", color: "#475569", display: "flex", alignItems: "center" }}
                >
                  {showPassword ? <EyeOff size={15} /> : <Eye size={15} />}
                </button>
              </div>
            </div>

            {/* Error */}
            {message && (
              <div style={{ padding: "11px 14px", borderRadius: 9, background: "rgba(244,63,94,0.1)", border: "1px solid rgba(244,63,94,0.25)", color: "#fb7185", fontSize: 13, fontWeight: 500 }}>
                {message}
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              className="btn-primary"
              disabled={loading}
              style={{ width: "100%", padding: "13px 20px", fontSize: 15, marginTop: 4 }}
            >
              {loading ? (
                <>
                  <span className="animate-spin" style={{ width: 16, height: 16, border: "2px solid rgba(255,255,255,0.3)", borderTopColor: "#fff", borderRadius: "50%", display: "inline-block" }} />
                  Authenticating...
                </>
              ) : (
                <>
                  Sign In to Portal
                  <ArrowRight size={16} />
                </>
              )}
            </button>
          </form>

          <div style={{ marginTop: 28, textAlign: "center", fontSize: 13, color: "#334155" }}>
            Don't have an account?{" "}
            <Link to="/register" style={{ color: "#818cf8", fontWeight: 600, textDecoration: "none" }}>
              Request Access →
            </Link>
          </div>

          {/* Security badge */}
          <div style={{ marginTop: 32, display: "flex", alignItems: "center", justifyContent: "center", gap: 16 }}>
            {["JWT Secured", "AES-256", "TLS 1.3"].map(label => (
              <div key={label} style={{ display: "flex", alignItems: "center", gap: 5, fontSize: 11, color: "#334155" }}>
                <ShieldCheck size={11} color="#334155" />
                {label}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}