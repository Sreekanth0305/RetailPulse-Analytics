import { useEffect, useState } from "react";

import NotificationsIcon from "@mui/icons-material/Notifications";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

import { useNavigate } from "react-router-dom";

import { getCurrentUser } from "../services/authService";

import { Badge } from "@mui/material";
import { getUnreadCount } from "../services/notificationService";

import "../styles/navbar.css";

function Navbar() {

    const navigate = useNavigate();

    const [user, setUser] = useState({

        name: "",

        role: ""

    });

    const [unreadCount, setUnreadCount] =
    useState(0);

    const loadCurrentUser = async () => {

        try {

            const response = await getCurrentUser();

            setUser(response.data);

        }

        catch (error) {

            console.log(error);

        }

    };

    const loadUnreadCount = async () => {

        try {
    
            const count =
                await getUnreadCount();
    
            setUnreadCount(count);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    useEffect(() => {

        loadCurrentUser();

        loadUnreadCount();

        const interval = setInterval(() => {

        loadUnreadCount();

        }, 5000);
    
        return () => clearInterval(interval);

    }, []);

    return (

        <div className="navbar">

            <h2>
                RetailPulse Analytics
            </h2>

            <div className="navbar-right">

                <Badge
                    badgeContent={unreadCount}
                    color="error"
                >
                
                    <NotificationsIcon
                
                        style={{
                            cursor: "pointer"
                        }}
                
                        onClick={() =>
                            navigate("/notifications")
                        }
                
                    />
                
                </Badge>

                <div
                    className="profile"
                    onClick={() => navigate("/profile")}
                >

                    <AccountCircleIcon fontSize="large" />

                    <div>

                        <h4>
                            {user.name}
                        </h4>

                        <p>
                            {user.role}
                        </p>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default Navbar;