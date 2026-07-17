import {
  Dashboard,
  People,
  Business,
  Category,
  Inventory,
  Analytics,
  Notifications,
  Settings,
  Logout,
  Person,
  History
} from "@mui/icons-material";

import { useNavigate } from "react-router-dom";

import "../styles/sidebar.css";

function Sidebar() {

  const navigate = useNavigate();

  const logout = () => {

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    navigate("/");

  };

  return (

    <div className="sidebar">

      <h2 className="logo">
        RetailPulse
      </h2>

      <ul>

        <li onClick={() => navigate("/dashboard")}>
          <Dashboard />
          <span>Dashboard</span>
        </li>

        <li>
          <People />
          <span>Employees</span>
        </li>

        <li>
          <Business />
          <span>Companies</span>
        </li>

        <li onClick={() => navigate("/categories")}>

            <Category />
        
            <span>Categories</span>
        
        </li>

        <li onClick={() => navigate("/products")}>

            <Inventory />
        
            <span>Products</span>
        
        </li>

        <li>
          <Analytics />
          <span>Analytics</span>
        </li>

        <li>
          <Notifications />
          <span>Notifications</span>
        </li>

        <li onClick={() => navigate("/profile")}>
          <Person />
          <span>Profile</span>
        </li>

        <li onClick={() => navigate("/audit-logs")}>
          <History />
          <span>Audit Logs</span>
        </li>

        <li>
          <Settings />
          <span>Settings</span>
        </li>

        <li onClick={logout}>
          <Logout />
          <span>Logout</span>
        </li>

      </ul>

    </div>

  );

}

export default Sidebar;