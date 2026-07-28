import axios from "../api/axios";

// =========================================
// Get All Customers
// =========================================
export const getCustomers = (
    filters: {
        search?: string;
        customer_type?: string;
        status?: string;
        city?: string;
        state?: string;
        country?: string;
        registration_date?: string;
        sort_by?: string;
    } = {}
) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/customers/", {

        headers: {

            Authorization: `Bearer ${token}`

        },

        params: filters

    });

};

// =========================================
// Get Customer By ID
// =========================================
export const getCustomerById = (customerId: number) => {

    const token = localStorage.getItem("access_token");

    return axios.get(`/customers/${customerId}`, {

        headers: {

            Authorization: `Bearer ${token}`

        }

    });

};

// =========================================
// Create Customer
// =========================================
export const createCustomer = (customer: any) => {

    const token = localStorage.getItem("access_token");

    return axios.post(

        "/customers/",

        customer,

        {

            headers: {

                Authorization: `Bearer ${token}`

            }

        }

    );

};

// =========================================
// Update Customer
// =========================================
export const updateCustomer = (

    customerId: number,

    customer: any

) => {

    const token = localStorage.getItem("access_token");

    return axios.put(

        `/customers/${customerId}`,

        customer,

        {

            headers: {

                Authorization: `Bearer ${token}`

            }

        }

    );

};

// =========================================
// Delete Customer
// =========================================
export const deleteCustomer = (

    customerId: number

) => {

    const token = localStorage.getItem("access_token");

    return axios.delete(

        `/customers/${customerId}`,

        {

            headers: {

                Authorization: `Bearer ${token}`

            }

        }

    );

};

// =========================================
// Activate / Deactivate Customer
// =========================================
export const changeCustomerStatus = (

    customerId: number,

    status: string

) => {

    const token = localStorage.getItem("access_token");

    return axios.put(

        `/customers/${customerId}/status?status=${status}`,

        {},

        {

            headers: {

                Authorization: `Bearer ${token}`

            }

        }

    );

};

export const getCustomerAnalytics = () => {

    const token = localStorage.getItem("access_token");

    return axios.get(
        "/customers/analytics",
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

};