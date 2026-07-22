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
  History,
  PointOfSale,
  Warehouse
} from "@mui/icons-material";

import { useNavigate } from "react-router-dom";

import { logout as logoutUser } from "../services/authService";

import "../styles/sidebar.css";

function Sidebar() {

  const navigate = useNavigate();

  const logout = async () => {

    try {

        await logoutUser();

    } catch (error) {

        console.log(error);

    }

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

        <li onClick={() => navigate("/sales")}>

            <PointOfSale />
        
            <span>Sales</span>
        
        </li>

        <li onClick={() => navigate("/inventory")}>

            <Warehouse />
        
            <span>Inventory</span>
        
        </li>

        <li>
          <Analytics />
          <span>Analytics</span>
        </li>

        <li onClick={() => navigate("/notifications")}>

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