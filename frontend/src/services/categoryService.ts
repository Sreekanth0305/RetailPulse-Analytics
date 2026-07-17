import axios from "../api/axios";

// -----------------------------
// Get All Categories
// -----------------------------
export const getCategories = () => {

    return axios.get("/categories/", {

        headers: {

            Authorization:
                `Bearer ${localStorage.getItem("access_token")}`

        }

    });

};


// -----------------------------
// Create Category
// -----------------------------
export const createCategory = (category: any) => {

    return axios.post(

        "/categories/",
        category,

        {

            headers: {

                Authorization:
                    `Bearer ${localStorage.getItem("access_token")}`

            }

        }

    );

};


// -----------------------------
// Update Category
// -----------------------------
export const updateCategory = (

    id: number,
    category: any

) => {

    return axios.put(

        `/categories/${id}`,
        category,

        {

            headers: {

                Authorization:
                    `Bearer ${localStorage.getItem("access_token")}`

            }

        }

    );

};


// -----------------------------
// Delete Category
// -----------------------------
export const deleteCategory = (

    id: number

) => {

    return axios.delete(

        `/categories/${id}`,

        {

            headers: {

                Authorization:
                    `Bearer ${localStorage.getItem("access_token")}`

            }

        }

    );

};


// -----------------------------
// Search Categories
// -----------------------------
export const searchCategory = (

    keyword: string

) => {

    return axios.get(

        `/categories/search?keyword=${keyword}`,

        {

            headers: {

                Authorization:
                    `Bearer ${localStorage.getItem("access_token")}`

            }

        }

    );

};