export interface User {
  username: string;

  email: string;

  role: "Admin" | "Analyst";

  created_at: string;

  status: string;
}

export interface UpdateRoleRequest {
  role: "Admin" | "Analyst";
}
