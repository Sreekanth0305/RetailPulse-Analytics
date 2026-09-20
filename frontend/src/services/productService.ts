import axios from "../api/axios";

const getAuthHeaders = () => {
    const token = localStorage.getItem("access_token");

    return {
        Authorization: `Bearer ${token}`
    };
};
export const getProducts = () => {

    return axios.get(

        "/products",

        {

            headers: getAuthHeaders()

        }

    );

};

export const createProduct = (data: any) => {

    return axios.post(

        "/products",

        data,

        {

            headers: getAuthHeaders()

        }

    );

};

export const updateProduct = (
    id: number,
    data: any
) => {

    return axios.put(
        `/products/${id}`,
        data,
        {
            headers: getAuthHeaders()
        }
    );

};

export const deleteProduct = (
    id: number
) => {

    return axios.delete(
        `/products/${id}`,
        {
            headers: getAuthHeaders()
        }
    );

};

export const searchProduct = (
    keyword: string
) => {

    return axios.get(
        `/products/search?keyword=${keyword}`,
        {
            headers: getAuthHeaders()
        }
    );

};

export const filterProduct = (
    categoryId: string,
    brand: string,
    status: string
) => {

    return axios.get(
        `/products/filter?category_id=${categoryId}&brand=${brand}&status=${status}`,
        {
            headers: getAuthHeaders()
        }
    );

};

export const activateProduct = (
    id: number
) => {

    return axios.patch(
        `/products/${id}/activate`,
        {},
        {
            headers: getAuthHeaders()
        }
    );

};

export const deactivateProduct = (
    id: number
) => {

    return axios.patch(
        `/products/${id}/deactivate`,
        {},
        {
            headers: getAuthHeaders()
        }
    );

};

export const sortProduct = (
    sortBy: string
) => {

    return axios.get(
        `/products/sort?sort_by=${sortBy}`,
        {
            headers: getAuthHeaders()
        }
    );

};