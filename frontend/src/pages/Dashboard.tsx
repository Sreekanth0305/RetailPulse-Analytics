import { useEffect, useState } from "react";

import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    PieChart,
    Pie,
    Cell,
    Legend
} from "recharts";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import { getDashboard,} from "../services/dashboardService";

import "../styles/dashboard.css";

function Dashboard(){

    const [dashboard, setDashboard] = useState({
        // Employee
        total_employees: 0,
        active_employees: 0,
        departments: 0,
        attendance: 0,

        // Product
        total_products: 0,
        active_products: 0,
        inactive_products: 0,
        total_categories: 0,

        // Sales
        total_sales: 0,
        total_revenue: 0,
        total_orders: 0,
        average_order_value: 0,

        // Inventory
        total_inventory_products: 0,
        total_inventory_quantity: 0,
        low_stock_products: 0,
        out_of_stock_products: 0,

        inventory_by_category: [],

        stock_status_distribution: []
    });


    const loadDashboard = async () => {

        try {
    
            const response = await getDashboard();
    
            setDashboard(response.data);
    
        } catch (error) {
    
            console.log(error);
    
        }
    
    };


    useEffect(() => {
    
        loadDashboard();
    
    }, []);

    const COLORS = [
    "#1976d2",
    "#2e7d32",
    "#ed6c02",
    "#d32f2f",
    "#7b1fa2",
    "#0288d1"
    ];

    return(

        <>

            <Sidebar/>

            <Navbar/>

            <div className="dashboard">

                <div className="cards">

                    <div className="card">

                        <h3>Total Employees</h3>

                        <h1>{dashboard.total_employees}</h1>

                    </div>

                    <div className="card">

                        <h3>Active Employees</h3>

                        <h1>{dashboard.active_employees}</h1>

                    </div>

                    <div className="card">

                        <h3>Departments</h3>

                        <h1>{dashboard.departments}</h1>

                    </div>

                    <div className="card">

                        <h3>Attendance</h3>

                        <h1>{dashboard.attendance}%</h1>

                    </div>

                </div>

                <h2 className="section-title">
                    Product Summary
                </h2>
                
                <div className="cards">
                
                    <div className="card">
                
                        <h3>Total Products</h3>
                
                        <h1>{dashboard.total_products}</h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Active Products</h3>
                
                        <h1>{dashboard.active_products}</h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Inactive Products</h3>
                
                        <h1>{dashboard.inactive_products}</h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Total Categories</h3>
                
                        <h1>{dashboard.total_categories}</h1>
                
                    </div>
                
                </div>

                <h2 className="section-title">
                    Sales Summary
                </h2>
                
                <div className="cards">
                
                    <div className="card">
                
                        <h3>Total Sales</h3>
                
                        <h1>
                            ₹{dashboard.total_sales.toLocaleString()}
                        </h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Total Revenue</h3>
                
                        <h1>
                            ₹{dashboard.total_revenue.toLocaleString()}
                        </h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Total Orders</h3>
                
                        <h1>
                            {dashboard.total_orders}
                        </h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Average Order Value</h3>
                
                        <h1>
                            ₹
                            {Number(
                                dashboard.average_order_value
                            ).toFixed(2)}
                        </h1>
                
                    </div>
                
                </div>

                <h2 className="section-title">
                    Inventory Summary
                </h2>

                <div className="cards">

                    <div className="card">
                
                        <h3>Total Inventory Products</h3>
                
                        <h1>{dashboard.total_inventory_products}</h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Total Inventory Quantity</h3>
                
                        <h1>{dashboard.total_inventory_quantity}</h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Low Stock Products</h3>
                
                        <h1>{dashboard.low_stock_products}</h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Out Of Stock Products</h3>
                
                        <h1>{dashboard.out_of_stock_products}</h1>
                
                    </div>
                
                </div>

                <h2 className="section-title">
                    Inventory Charts
                </h2>
                
                <div className="dashboard-charts">
                
                    <div className="chart-card">
                
                        <h3>Inventory by Category</h3>
                
                        <ResponsiveContainer
                            width="100%"
                            height={320}
                        >
                
                            <BarChart
                                data={dashboard.inventory_by_category}
                            >
                
                                <CartesianGrid strokeDasharray="3 3" />
                
                                <XAxis dataKey="category" />
                
                                <YAxis />
                
                                <Tooltip />
                
                                <Bar
                                    dataKey="quantity"
                                    fill="#1976d2"
                                />
                
                            </BarChart>
                
                        </ResponsiveContainer>
                
                    </div>
                
                    <div className="chart-card">
                
                        <h3>Stock Status Distribution</h3>
                
                        <ResponsiveContainer
                            width="100%"
                            height={320}
                        >
                
                            <PieChart>
                
                                <Pie
                
                                    data={dashboard.stock_status_distribution}
                
                                    dataKey="count"
                
                                    nameKey="status"
                
                                    outerRadius={100}
                
                                    label
                
                                >
                
                                    {
                
                                        dashboard.stock_status_distribution.map(
                
                                            (_: any, index: number) => (
                
                                                <Cell
                
                                                    key={index}
                
                                                    fill={COLORS[index % COLORS.length]}
                
                                                />
                
                                            )
                
                                        )
                
                                    }
                
                                </Pie>
                
                                <Tooltip />
                
                                <Legend />
                
                            </PieChart>
                
                        </ResponsiveContainer>
                
                    </div>
                
                </div>

            </div>

        </>

    );

}

export default Dashboard;