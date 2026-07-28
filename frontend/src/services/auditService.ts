import axios from "../api/axios";

export const getAuditLogs = () => {

    const token = localStorage.getItem("access_token");

    return axios.get("/audit-logs/", {

        headers: {

            Authorization: `Bearer ${token}`

        }

    });

};

export const createAuditLog = (data: any) => {

    const token = localStorage.getItem("access_token");

    return axios.post(
        "/audit-logs/",
        data,
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

};