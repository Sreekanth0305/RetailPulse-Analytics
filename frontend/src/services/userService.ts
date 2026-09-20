import axios from "../api/axios";


// =========================================
// Get All Users
// =========================================
export const getUsers = () => {

    const token = localStorage.getItem("access_token");

    return axios.get("/users/", {

        headers: {

            Authorization: `Bearer ${token}`

        }

    });

};