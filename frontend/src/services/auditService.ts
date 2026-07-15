import axios from "../api/axios";

export const getAuditLogs = () => {

    const token = localStorage.getItem("access_token");

    return axios.get("/audit-logs/", {

        headers: {

            Authorization: `Bearer ${token}`

        }

    });

};