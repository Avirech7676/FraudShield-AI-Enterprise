import type { DashboardKpis } from "../types/dashboard.ts";

type Props = {
  kpis: DashboardKpis;
};

export default function KpiCards({ kpis }: Props) {
  const cards = [
    {
      title: "Transactions",

      value: kpis.transactions,
    },

    {
      title: "Predictions",

      value: kpis.predictions,
    },

    {
      title: "Fraud Cases",

      value: kpis.fraud_cases,
    },

    {
      title: "Alerts",

      value: kpis.alerts,
    },

    {
      title: "Critical Alerts",

      value: kpis.critical_alerts,
    },

    {
      title: "Average Risk",

      value: kpis.average_risk,
    },

    {
      title: "Models Loaded",

      value: kpis.models_loaded,
    },

    {
      title: "Features Used",

      value: kpis.features_used,
    },
  ];

  return (
    <div className="summary-grid">
      {cards.map((card) => (
        <div className="summary-card" key={card.title}>
          <h4>{card.title}</h4>

          <h2>{card.value}</h2>
        </div>
      ))}
    </div>
  );
}
