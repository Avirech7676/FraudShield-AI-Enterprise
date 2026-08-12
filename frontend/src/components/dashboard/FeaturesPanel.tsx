type Props = {
  features: string[];
};

export default function FeaturesPanel({ features }: Props) {
  return (
    <div className="dashboard-card">
      <h3>Model Features</h3>

      <div className="feature-grid">
        {features.map((feature) => (
          <div key={feature} className="feature-chip">
            {feature}
          </div>
        ))}
      </div>
    </div>
  );
}
