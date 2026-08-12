type BadgeVariant = "success" | "danger" | "warning" | "info" | "secondary";

type Props = {
  children: React.ReactNode;
  variant: BadgeVariant;
};

export default function Badge({ children, variant }: Props) {
  return <span className={`badge badge-${variant}`}>{children}</span>;
}
