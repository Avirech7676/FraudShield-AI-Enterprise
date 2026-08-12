import type { User } from "../../types/user";

type Props = {
  user: User | null;
  onClose: () => void;
  onDelete: () => Promise<void> | void;
};

export default function DeleteUserDialog({ user, onClose, onDelete }: Props) {
  if (!user) return null;

  return (
    <div className="modal">
      <div className="modal-backdrop" onClick={onClose} />
      <div className="modal-content">
        <h3>Delete User</h3>
        <p>Are you sure you want to delete user {user.username}?</p>

        <div className="modal-actions">
          <button onClick={onClose}>Cancel</button>
          <button
            onClick={async () => {
              await onDelete();
            }}
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}
