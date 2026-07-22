import axios from "../api/axios";

const getToken = () => ({
    headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
    },
});

// ------------------------------
// Get Inventory
// ------------------------------
export const getInventory = () => {
    return axios.get(
        "/inventory/",
        getToken()
    );
};

// ------------------------------
// Get Inventory By Product
// ------------------------------
export const getInventoryByProduct = (
    productId: number
) => {
    return axios.get(
        `/inventory/${productId}`,
        getToken()
    );
};

// ------------------------------
// Search Inventory
// ------------------------------
export const searchInventory = (
    keyword: string
) => {
    return axios.get(
        `/inventory/search?keyword=${keyword}`,
        getToken()
    );
};

// ------------------------------
// Filter Inventory
// ------------------------------
export const filterInventory = (
    category?: number,
    brand?: string,
    status?: string
) => {

    const params = new URLSearchParams();

    if (category)
        params.append("category_id", category.toString());

    if (brand)
        params.append("brand", brand);

    if (status)
        params.append("stock_status", status);

    return axios.get(
        `/inventory/filter?${params.toString()}`,
        getToken()
    );
};

// ------------------------------
// Sort Inventory
// ------------------------------
export const sortInventory = (
    sortBy: string
) => {
    return axios.get(
        `/inventory/sort?sort_by=${sortBy}`,
        getToken()
    );
};

// ------------------------------
// Add Stock
// ------------------------------
export const addStock = (
    productId: number,
    data: any
) => {
    return axios.post(
        `/inventory/${productId}/add`,
        data,
        getToken()
    );
};

// ------------------------------
// Remove Stock
// ------------------------------
export const removeStock = (
    productId: number,
    data: any
) => {
    return axios.post(
        `/inventory/${productId}/remove`,
        data,
        getToken()
    );
};

// ------------------------------
// Manual Adjustment
// ------------------------------
export const adjustStock = (
    productId: number,
    data: any
) => {
    return axios.put(
        `/inventory/${productId}/adjust`,
        data,
        getToken()
    );
};

// ------------------------------
// Update Reorder Level
// ------------------------------
export const updateReorderLevel = (
    productId: number,
    data: any
) => {
    return axios.put(
        `/inventory/${productId}/reorder-level`,
        data,
        getToken()
    );
};

export const getInventoryMovements = (
    inventoryId: number
) => {

    const token = localStorage.getItem("access_token");

    return axios.get(

        `/inventory/${inventoryId}/movements`,

        {

            headers: {

                Authorization: `Bearer ${token}`

            }

        }

    );

};

export const getCategories = () => {

    const token = localStorage.getItem("access_token");

    return axios.get("/categories", {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};