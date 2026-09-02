import { Outlet } from "react-router-dom";
import Breadcrumbs from "../components/common/Breadcrumbs";
import Sidebar from "../components/layouts/Sidebar";
import Navbar from "../components/layouts/Navbar";

export default function DashboardLayout() {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="layout-main">
        <Navbar />
        <Breadcrumbs />
        <main className="layout-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}