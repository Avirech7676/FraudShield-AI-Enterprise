import React from "react";
import { TableSkeleton } from "./Skeleton";
import { EmptyState } from "./EmptyState";

export interface Column<T> {
  key: string;
  header: React.ReactNode;
  render?: (row: T, index: number) => React.ReactNode;
  align?: "left" | "center" | "right";
  width?: string;
}

export interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  isLoading?: boolean;
  emptyTitle?: string;
  emptyDescription?: string;
  onRowClick?: (row: T) => void;
  className?: string;
}

export function Table<T extends Record<string, any>>({
  columns,
  data,
  isLoading = false,
  emptyTitle,
  emptyDescription,
  onRowClick,
  className = "",
}: TableProps<T>) {
  if (isLoading) {
    return (
      <div className="p-6 bg-slate-900/60 border border-slate-800 rounded-2xl">
        <TableSkeleton rows={6} columns={columns.length} />
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <EmptyState
        title={emptyTitle || "No records match search criteria"}
        description={emptyDescription || "Try adjusting your query or filters."}
      />
    );
  }

  const alignClasses = {
    left: "text-left",
    center: "text-center",
    right: "text-right",
  };

  return (
    <div className={`w-full overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/60 backdrop-blur-xl shadow-xl ${className}`}>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-sm select-none">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-950/60">
              {columns.map((col) => (
                <th
                  key={col.key}
                  style={{ width: col.width }}
                  className={`px-5 py-3.5 text-xs font-semibold uppercase tracking-wider text-slate-400 ${
                    alignClasses[col.align || "left"]
                  }`}
                >
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/50">
            {data.map((row, idx) => (
              <tr
                key={row.id || row._id || idx}
                onClick={() => onRowClick?.(row)}
                className={`transition-colors hover:bg-slate-800/40 ${
                  onRowClick ? "cursor-pointer" : ""
                }`}
              >
                {columns.map((col) => (
                  <td
                    key={col.key}
                    className={`px-5 py-3.5 text-slate-200 ${
                      alignClasses[col.align || "left"]
                    }`}
                  >
                    {col.render ? col.render(row, idx) : row[col.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
