import NotificationsIcon from "@mui/icons-material/Notifications";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

import { useNavigate } from "react-router-dom";
import "../styles/navbar.css";

function Navbar() {

    const navigate = useNavigate();

    return (

        <div className="navbar">

            <h2>
                RetailPulse Analytics
            </h2>

            <div className="navbar-right">

                <NotificationsIcon />

                <div
                    className="profile"
                    onClick={() => navigate("/profile")}
                >

                    <AccountCircleIcon fontSize="large"/>

                    <div>

                        <h4>
                            Admin User
                        </h4>

                        <p>
                            Company Admin
                        </p>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default Navbar;