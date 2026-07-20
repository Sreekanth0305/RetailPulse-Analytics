import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import { getDashboard,} from "../services/dashboardService";

import "../styles/dashboard.css";

function Dashboard(){

    const [dashboard, setDashboard] = useState({
        total_employees: 0,
        active_employees: 0,
        departments: 0,
        attendance: 0,
    
        total_products: 0,
        active_products: 0,
        inactive_products: 0,
        total_categories: 0,
    
        total_sales: 0,
        total_revenue: 0,
        total_orders: 0,
        average_order_value: 0,
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

            </div>

        </>

    );

}

export default Dashboard;