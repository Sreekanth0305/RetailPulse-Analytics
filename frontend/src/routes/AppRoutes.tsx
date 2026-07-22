import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import RegisterCompany from "../pages/RegisterCompany";
import Profile from "../pages/Profile";
import AuditLogs from "../pages/AuditLogs";
import Categories from "../pages/Categories";
import Products from "../pages/Products";
import Sales from "../pages/Sales";
import SaleDetails from "../pages/SaleDetails";
import Notifications from "../pages/Notifications";
import Inventory from "../pages/Inventory";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/register" element={<RegisterCompany />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/audit-logs" element={<AuditLogs />}/>
        <Route path="/categories" element={<Categories />}/>
        <Route path="/products" element={<Products />} />
        <Route path="/sales" element={<Sales />} />
        <Route path="/sales/:saleId" element={<SaleDetails />}/>
        <Route path="/notifications" element={<Notifications />}/>
        <Route path="/inventory" element={<Inventory />}/>
      </Routes>
    </BrowserRouter>
  );
}