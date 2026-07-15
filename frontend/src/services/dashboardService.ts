import axios from "../api/axios";

export const getDashboard = () => {

    const token = localStorage.getItem("access_token");

    return axios.get("/dashboard", {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};