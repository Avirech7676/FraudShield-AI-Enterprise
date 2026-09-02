type Props = {
  title: string;

  value: number;
};

export default function UserCard({
  title,

  value,
}: Props) {
  return (
    <div className="summary-card">
      <h4>{title}</h4>

      <h2>{value}</h2>
    </div>
  );
}
