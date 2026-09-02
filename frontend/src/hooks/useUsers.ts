import { useEffect, useState } from "react";

import type { User } from "../types/user";

import { getUsers, deleteUser, updateUserRole } from "../services/users";

export function useUsers() {
  const [users, setUsers] = useState<User[]>([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  async function load() {
    try {
      setLoading(true);

      const response = await getUsers();

      setUsers(response);
    } catch (e) {
      if (e instanceof Error) {
        setError(e.message);
      }
    } finally {
      setLoading(false);
    }
  }

  async function remove(username: string) {
    await deleteUser(username);

    load();
  }

  async function changeRole(
    username: string,

    role: "Admin" | "Analyst",
  ) {
    await updateUserRole(username, role);

    load();
  }

  useEffect(() => {
    load();
  }, []);

  return {
    users,

    loading,

    error,

    refresh: load,

    remove,

    changeRole,
  };
}
