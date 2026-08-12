import type { User } from "../../types/user";
import { Table, type Column } from "../ui/Table";
import { Badge } from "../ui/Badge";
import { Button } from "../ui/Button";
import { Edit3, Trash2, ShieldCheck, UserCheck } from "lucide-react";

type Props = {
  users: User[];
  onEdit: (user: User) => void;
  onDelete: (user: User) => void;
};

export default function UserTable({ users, onEdit, onDelete }: Props) {
  const columns: Column<User>[] = [
    {
      key: "username",
      header: "Operational Handle",
      render: (row) => (
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-full bg-indigo-500/20 text-indigo-300 font-bold flex items-center justify-center text-xs">
            {row.username[0].toUpperCase()}
          </div>
          <span className="font-semibold text-slate-100">{row.username}</span>
        </div>
      ),
    },
    {
      key: "email",
      header: "Corporate Email",
      render: (row) => (
        <span className="text-xs text-slate-300 font-mono">{row.email}</span>
      ),
    },
    {
      key: "role",
      header: "Security Role",
      render: (row) => (
        <Badge variant={row.role === "Admin" ? "purple" : "indigo"} size="sm">
          {row.role === "Admin" ? <ShieldCheck className="w-3 h-3" /> : <UserCheck className="w-3 h-3" />}
          {row.role}
        </Badge>
      ),
    },
    {
      key: "status",
      header: "Account Status",
      render: (row) => (
        <Badge variant={row.status === "Inactive" ? "rose" : "emerald"} size="sm" dot>
          {row.status || "Active"}
        </Badge>
      ),
    },
    {
      key: "created_at",
      header: "Provisioned Date",
      align: "right",
      render: (row) => (
        <span className="text-xs text-slate-400">
          {row.created_at ? new Date(row.created_at).toLocaleDateString() : "Active"}
        </span>
      ),
    },
    {
      key: "actions",
      header: "Action",
      align: "right",
      render: (row) => (
        <div className="flex items-center justify-end gap-2" onClick={(e) => e.stopPropagation()}>
          <Button
            variant="ghost"
            size="sm"
            leftIcon={<Edit3 className="w-3.5 h-3.5" />}
            onClick={() => onEdit(row)}
          >
            Role
          </Button>

          <Button
            variant="danger"
            size="sm"
            leftIcon={<Trash2 className="w-3.5 h-3.5" />}
            onClick={() => onDelete(row)}
          >
            Revoke
          </Button>
        </div>
      ),
    },
  ];

  return (
    <Table
      columns={columns}
      data={users}
      emptyTitle="No Operational Users Found"
      emptyDescription="No analyst or administrator accounts match your active search query."
    />
  );
}
