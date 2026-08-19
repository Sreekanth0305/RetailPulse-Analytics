import axios from "../api/axios";


const getAuthHeaders = () => {

    const token =
        localStorage.getItem("access_token");

    return {
        Authorization: `Bearer ${token}`,
    };
};


// =========================================================
// Inventory Forecast
// =========================================================

export const getInventoryForecast = (
    params: any = {}
) => {

    return axios.get(
        "/inventory/forecast",
        {
            params,
            headers: getAuthHeaders()
        }
    );
};


// =========================================================
// Inventory Recommendations
// =========================================================

export const getInventoryRecommendations = (
    params: any = {}
) => {

    return axios.get(
        "/inventory/recommendations",
        {
            params,
            headers: getAuthHeaders()
        }
    );
};


// =========================================================
// Single Product Recommendation
// =========================================================

export const getProductInventoryRecommendation = (
    productId: number,
    params: any = {}
) => {

    return axios.get(
        `/inventory/recommendations/${productId}`,
        {
            params,
            headers: getAuthHeaders()
        }
    );
};