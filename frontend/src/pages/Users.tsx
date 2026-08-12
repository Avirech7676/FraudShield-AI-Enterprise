import { useMemo, useState } from "react";
import { useUsers } from "../hooks/useUsers";
import UserTable from "../components/users/UserTable";
import EditRoleModal from "../components/users/EditRoleModal";
import DeleteUserDialog from "../components/users/DeleteUserDialog";
import type { User } from "../types/user";

import { MetricCard } from "../components/ui/MetricCard";
import { Input } from "../components/ui/Input";
import { Select } from "../components/ui/Select";
import { Button } from "../components/ui/Button";
import { Skeleton } from "../components/ui/Skeleton";
import { ErrorState } from "../components/ui/ErrorState";
import { Users as UsersIcon, ShieldCheck, UserCheck, Activity, Search, ChevronLeft, ChevronRight } from "lucide-react";

const PAGE_SIZE = 10;

export default function UsersPage() {
  const { users, loading, error, refresh, remove, changeRole } = useUsers();

  const [search, setSearch] = useState("");
  const [role, setRole] = useState("");
  const [page, setPage] = useState(1);
  const [editUser, setEditUser] = useState<User | null>(null);
  const [deleteUser, setDeleteUser] = useState<User | null>(null);

  const safeUsers = useMemo(() => {
    return Array.isArray(users) ? users : [];
  }, [users]);

  const filtered = useMemo(() => {
    return safeUsers.filter((user) => {
      const searchMatch =
        (user.username || "").toLowerCase().includes(search.toLowerCase()) ||
        (user.email || "").toLowerCase().includes(search.toLowerCase());

      const roleMatch = role === "" || user.role === role;
      return searchMatch && roleMatch;
    });
  }, [safeUsers, search, role]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const paginated = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  const totalUsers = safeUsers.length;
  const admins = safeUsers.filter((u) => u.role === "Admin").length;
  const analysts = safeUsers.filter((u) => u.role === "Analyst").length;
  const active = safeUsers.filter((u) => u.status !== "Inactive").length;

  if (loading) {
    return (
      <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
        <div className="grid-4">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} variant="card" className="h-28" />
          ))}
        </div>
        <Skeleton variant="rectangular" className="h-96 w-full" />
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: "40px 0" }}>
        <ErrorState
          title="User Directory Error"
          message={error}
          onRetry={refresh}
        />
      </div>
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }} className="animate-fade-in">
      {/* Subheader Toolbar */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, paddingBottom: 16, borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ width: 36, height: 36, borderRadius: 10, background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.25)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <UsersIcon size={18} color="#818cf8" />
          </div>
          <div>
            <h2 style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9", margin: 0 }}>
              Enterprise Access &amp; User Directory
            </h2>
            <p style={{ fontSize: 12, color: "#475569", margin: "2px 0 0" }}>
              Operator accounts, role assignments, security permissions &amp; access status
            </p>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid-4">
        <MetricCard
          title="Total User Accounts"
          value={totalUsers}
          icon={<UsersIcon className="w-5 h-5 text-indigo-400" />}
        />
        <MetricCard
          title="System Administrators"
          value={admins}
          icon={<ShieldCheck className="w-5 h-5 text-rose-400" />}
        />
        <MetricCard
          title="Security Analysts"
          value={analysts}
          icon={<UserCheck className="w-5 h-5 text-amber-400" />}
        />
        <MetricCard
          title="Active Sessions"
          value={active}
          icon={<Activity className="w-5 h-5 text-emerald-400" />}
        />
      </div>

      {/* Filter Controls */}
      <div className="fs-card" style={{ padding: 16, display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, flexWrap: "wrap" }}>
        <div style={{ flex: 1, minWidth: 260, maxWidth: 360 }}>
          <Input
            placeholder="Search username or email..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            leftIcon={<Search className="w-4 h-4" />}
          />
        </div>

        <div style={{ width: 180 }}>
          <Select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            options={[
              { value: "", label: "All Access Roles" },
              { value: "Admin", label: "Admin Role Only" },
              { value: "Analyst", label: "Analyst Role Only" },
            ]}
          />
        </div>
      </div>

      {/* User Table */}
      <div className="fs-card" style={{ overflow: "hidden" }}>
        <UserTable
          users={paginated}
          onEdit={(u) => setEditUser(u)}
          onDelete={(u) => setDeleteUser(u)}
        />
      </div>

      {/* Pagination Controls */}
      <div className="fs-card" style={{ padding: "12px 20px", display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, fontSize: 13, color: "#64748b" }}>
        <span>
          Showing {filtered.length === 0 ? 0 : (page - 1) * PAGE_SIZE + 1}-
          {Math.min(page * PAGE_SIZE, filtered.length)} of {filtered.length} total users
        </span>

        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <Button
            variant="outline"
            size="sm"
            disabled={page <= 1}
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            leftIcon={<ChevronLeft className="w-4 h-4" />}
          >
            Previous
          </Button>

          <span style={{ fontWeight: 600, color: "#e2e8f0", padding: "0 8px" }}>
            Page {page} of {totalPages}
          </span>

          <Button
            variant="outline"
            size="sm"
            disabled={page >= totalPages}
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            rightIcon={<ChevronRight className="w-4 h-4" />}
          >
            Next
          </Button>
        </div>
      </div>

      {/* Edit Role Modal */}
      {editUser && (
        <EditRoleModal
          user={editUser}
          onClose={() => setEditUser(null)}
          onSave={async (newRole) => {
            await changeRole(editUser.username, newRole as "Admin" | "Analyst");
            setEditUser(null);
          }}
        />
      )}

      {/* Delete User Dialog */}
      {deleteUser && (
        <DeleteUserDialog
          user={deleteUser}
          onClose={() => setDeleteUser(null)}
          onDelete={async () => {
            await remove(deleteUser.username);
            setDeleteUser(null);
          }}
        />
      )}
    </div>
  );
}
