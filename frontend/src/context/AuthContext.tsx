import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";
import type { ReactNode } from "react";

type User = {
  username: string;
  role: string;
};

type AuthContextType = {
  token: string | null;
  user: User | null;
  login: (token: string, username: string, role: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
  /** True while AuthProvider is still reading localStorage on first mount */
  loading: boolean;
};

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);

  // Start loading=true so ProtectedRoute waits before deciding to redirect.
  // This prevents the race condition where isAuthenticated=false briefly on
  // page load before localStorage has been read.
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    const username = localStorage.getItem("username");
    const role = localStorage.getItem("role");

    if (storedToken && username && role) {
      setToken(storedToken);
      setUser({ username, role });
    }

    // Auth state fully restored from storage — release the hold.
    setLoading(false);
  }, []);

  function login(jwt: string, username: string, role: string) {
    localStorage.setItem("token", jwt);
    localStorage.setItem("username", username);
    localStorage.setItem("role", role);

    setToken(jwt);
    setUser({ username, role });
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("role");

    setToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        login,
        logout,
        isAuthenticated: !!token,
        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}
