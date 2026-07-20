import axios from "../api/axios";

const token = localStorage.getItem("access_token");

export const getProducts = () => {

    return axios.get(

        "/products",

        {

            headers: {

                Authorization: `Bearer ${token}`

            }

        }

    );

};

export const createProduct = (data: any) => {

    return axios.post(

        "/products",

        data,

        {

            headers: {

                Authorization: `Bearer ${token}`

            }

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

            headers: {

                Authorization: `Bearer ${token}`

            }

        }

    );

};

export const deleteProduct = (

    id: number

) => {

    return axios.delete(

        `/products/${id}`,

        {

            headers: {

                Authorization: `Bearer ${token}`

            }

        }

    );

};

export const searchProduct = (

    keyword: string

) => {

    return axios.get(

        `/products/search?keyword=${keyword}`,

        {

            headers: {

                Authorization: `Bearer ${token}`

            }

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

            headers: {

                Authorization: `Bearer ${token}`

            }

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

            headers: {

                Authorization: `Bearer ${token}`

            }

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

            headers: {

                Authorization: `Bearer ${token}`

            }

        }

    );

};

export const sortProduct = (

    sortBy: string

) => {

    return axios.get(

        `/products/sort?sort_by=${sortBy}`,

        {

            headers: {

                Authorization: `Bearer ${token}`

            }

        }

    );

};