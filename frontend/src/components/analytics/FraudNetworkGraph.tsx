import { useState } from "react";
import { Network, Cpu, Laptop, CreditCard, User, Globe } from "lucide-react";
import { Badge } from "../ui/Badge";

interface Node {
  id: string;
  type: "account" | "device" | "ip" | "card";
  label: string;
  risk: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  details: string;
  x: number;
  y: number;
}

interface Edge {
  source: string;
  target: string;
  label: string;
}

export function FraudNetworkGraph() {
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);

  const nodes: Node[] = [
    { id: "usr_1", type: "account", label: "User #8492 (Avinash)", risk: "HIGH", details: "3 Linked Chargebacks", x: 120, y: 80 },
    { id: "usr_2", type: "account", label: "User #9103 (Suspect)", risk: "HIGH", details: "Location Jump detected", x: 120, y: 220 },
    { id: "dev_1", type: "device", label: "Device #DEV-99X", risk: "HIGH", details: "Rooted Android Emulator", x: 320, y: 150 },
    { id: "ip_1",  type: "ip",     label: "IP 185.220.101.4", risk: "CRITICAL", details: "TOR Exit Node (Russian Federation)", x: 520, y: 150 },
    { id: "card_1",type: "card",   label: "Card **** 4892", risk: "HIGH", details: "Cross-account Card Reuse", x: 320, y: 280 },
    { id: "usr_3", type: "account", label: "User #4412 (Normal)", risk: "LOW", details: "Legitimate Account History", x: 520, y: 280 },
  ];

  const edges: Edge[] = [
    { source: "usr_1", target: "dev_1", label: "Logged In" },
    { source: "usr_2", target: "dev_1", label: "Shared Device" },
    { source: "dev_1", target: "ip_1", label: "TOR Connection" },
    { source: "usr_1", target: "card_1", label: "Card Used" },
    { source: "usr_2", target: "card_1", label: "Shared Card" },
    { source: "usr_3", target: "card_1", label: "Authorized User" },
  ];

  const getNodeColor = (risk: string) => {
    switch (risk) {
      case "CRITICAL": return "#f43f5e";
      case "HIGH": return "#fb7185";
      case "MEDIUM": return "#f59e0b";
      default: return "#10b981";
    }
  };

  const getNodeIcon = (type: string) => {
    switch (type) {
      case "account": return <User size={14} color="#fff" />;
      case "device": return <Laptop size={14} color="#fff" />;
      case "ip": return <Globe size={14} color="#fff" />;
      case "card": return <CreditCard size={14} color="#fff" />;
      default: return <Cpu size={14} color="#fff" />;
    }
  };

  return (
    <div className="fs-card" style={{ padding: 24 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 34, height: 34, borderRadius: 10, background: "rgba(244,63,94,0.15)", border: "1px solid rgba(244,63,94,0.3)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Network size={18} color="#fb7185" />
          </div>
          <div>
            <div style={{ fontSize: 15, fontWeight: 700, color: "#f1f5f9" }}>
              Fraud Ring &amp; Shared Device Network Graph
            </div>
            <div style={{ fontSize: 12, color: "#64748b" }}>
              Real-time entity relationship mapping &amp; TOR exit node clustering
            </div>
          </div>
        </div>

        <Badge variant="rose" size="md" dot pulse>
          Fraud Ring Active
        </Badge>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 20, alignItems: "start" }}>
        {/* SVG Graph Canvas */}
        <div style={{ position: "relative", background: "rgba(0,0,0,0.4)", borderRadius: 14, border: "1px solid rgba(255,255,255,0.06)", height: 360, overflow: "hidden" }}>
          <svg style={{ width: "100%", height: "100%" }}>
            {/* Draw Edges */}
            {edges.map((edge, idx) => {
              const srcNode = nodes.find(n => n.id === edge.source);
              const tgtNode = nodes.find(n => n.id === edge.target);
              if (!srcNode || !tgtNode) return null;

              return (
                <g key={idx}>
                  <line
                    x1={srcNode.x}
                    y1={srcNode.y}
                    x2={tgtNode.x}
                    y2={tgtNode.y}
                    stroke="rgba(99,102,241,0.4)"
                    strokeWidth="2"
                    strokeDasharray="4 2"
                  />
                </g>
              );
            })}

            {/* Draw Nodes */}
            {nodes.map((node) => {
              const isSelected = selectedNode?.id === node.id;
              const color = getNodeColor(node.risk);

              return (
                <g
                  key={node.id}
                  transform={`translate(${node.x}, ${node.y})`}
                  onClick={() => setSelectedNode(node)}
                  style={{ cursor: "pointer" }}
                >
                  <circle
                    r={isSelected ? 22 : 18}
                    fill={color}
                    opacity="0.25"
                    stroke={color}
                    strokeWidth="2"
                  />
                  <circle
                    r={12}
                    fill="#0f172a"
                    stroke={color}
                    strokeWidth="2"
                  />
                  <text
                    y={30}
                    textAnchor="middle"
                    fill="#cbd5e1"
                    fontSize="11"
                    fontWeight="600"
                  >
                    {node.label}
                  </text>
                </g>
              );
            })}
          </svg>

          <div style={{ position: "absolute", bottom: 12, left: 12, display: "flex", gap: 12, fontSize: 11, color: "#64748b", background: "rgba(2,4,10,0.8)", padding: "6px 12px", borderRadius: 8, border: "1px solid rgba(255,255,255,0.06)" }}>
            <span style={{ display: "flex", alignItems: "center", gap: 4 }}><span style={{ width: 8, height: 8, borderRadius: "50%", background: "#f43f5e" }} /> Critical</span>
            <span style={{ display: "flex", alignItems: "center", gap: 4 }}><span style={{ width: 8, height: 8, borderRadius: "50%", background: "#fb7185" }} /> High Risk</span>
            <span style={{ display: "flex", alignItems: "center", gap: 4 }}><span style={{ width: 8, height: 8, borderRadius: "50%", background: "#10b981" }} /> Low Risk</span>
          </div>
        </div>

        {/* Selected Entity Inspector */}
        <div style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.06)", borderRadius: 14, padding: 18, minHeight: 360 }}>
          {selectedNode ? (
            <div style={{ display: "flex", flexDirection: "column", gap: 14 }} className="animate-fade-in">
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <Badge variant={selectedNode.risk === "CRITICAL" ? "rose" : selectedNode.risk === "HIGH" ? "rose" : "emerald"} size="sm">
                  {selectedNode.risk} RISK
                </Badge>
                <span style={{ fontSize: 11, color: "#64748b", fontFamily: "var(--font-mono)" }}>{selectedNode.id}</span>
              </div>

              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <div style={{ padding: 6, borderRadius: 8, background: "rgba(99,102,241,0.15)" }}>
                  {getNodeIcon(selectedNode.type)}
                </div>
                <div>
                  <div style={{ fontSize: 15, fontWeight: 700, color: "#f1f5f9" }}>{selectedNode.label}</div>
                  <div style={{ fontSize: 12, color: "#94a3b8", marginTop: 2 }}>Type: {selectedNode.type.toUpperCase()}</div>
                </div>
              </div>

              <div style={{ padding: 12, borderRadius: 10, background: "rgba(0,0,0,0.3)", border: "1px solid rgba(255,255,255,0.05)", fontSize: 12, color: "#cbd5e1" }}>
                <strong>Attribution Details:</strong><br />
                {selectedNode.details}
              </div>

              <div style={{ fontSize: 12, color: "#64748b", lineHeight: 1.5 }}>
                Shared device fingerprints and card numbers across multiple user accounts indicate a coordinated syndicate.
              </div>
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100%", textAlign: "center", color: "#475569", minHeight: 320 }}>
              <Network size={36} style={{ opacity: 0.3, marginBottom: 10 }} />
              <div style={{ fontSize: 13, fontWeight: 600, color: "#64748b" }}>Inspect Cluster Node</div>
              <div style={{ fontSize: 11, marginTop: 4 }}>Click any node on the graph canvas to inspect shared device &amp; credit card vectors</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
