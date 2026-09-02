type Props = {
  search: string;
  setSearch: (value: string) => void;

  role: string;
  setRole: (value: string) => void;
};

export default function UserFilters({
  search,
  setSearch,
  role,
  setRole,
}: Props) {
  return (
    <div className="user-filters">
      <input
        placeholder="Search username..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <select value={role} onChange={(e) => setRole(e.target.value)}>
        <option value="">All Roles</option>
        <option value="Admin">Admin</option>
        <option value="Analyst">Analyst</option>
      </select>
    </div>
  );
}
