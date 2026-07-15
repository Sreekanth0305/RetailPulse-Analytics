import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import { getDashboard } from "../services/dashboardService";

import "../styles/dashboard.css";

function Dashboard(){

    const [dashboard, setDashboard] = useState({
    total_employees: 0,
    active_employees: 0,
    departments: 0,
    attendance: 0
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

            </div>

        </>

    );

}

export default Dashboard;