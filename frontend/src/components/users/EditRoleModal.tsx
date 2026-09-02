import type { User } from "../../types/user";
import { useState } from "react";

type Role = "Admin" | "Analyst";

type Props = {
  user: User | null;
  onClose: () => void;
  onSave: (newRole: Role) => Promise<void> | void;
};

export default function EditRoleModal({ user, onClose, onSave }: Props) {
  const [role, setRole] = useState<Role>((user?.role as Role) ?? "Analyst");

  if (!user) return null;

  return (
    <div className="modal">
      <div className="modal-backdrop" onClick={onClose} />
      <div className="modal-content">
        <h3>Edit Role - {user.username}</h3>

        <select value={role} onChange={(e) => setRole(e.target.value as Role)}>
          <option value="Admin">Admin</option>
          <option value="Analyst">Analyst</option>
        </select>

        <div className="modal-actions">
          <button onClick={onClose}>Cancel</button>
          <button
            onClick={async () => {
              await onSave(role);
            }}
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
}
