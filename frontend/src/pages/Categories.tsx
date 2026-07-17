import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import { getCategories } from "../services/categoryService";
import { deleteCategory } from "../services/categoryService";
import CategoryForm from "../components/CategoryForm";
import { searchCategory } from "../services/categoryService";

import "../styles/categories.css";

function Categories() {

    const [categories, setCategories] = useState<any[]>([]);

    const [keyword, setKeyword] = useState("");

    const [open, setOpen] = useState(false);

    const [selectedCategory, setSelectedCategory] = useState<any>(null);

    const loadCategories = async () => {

        try {

            const response = await getCategories();

            setCategories(response.data);

        }
        catch (error) {

            console.log(error);

        }

    };

    useEffect(() => {

        loadCategories();

    }, []);

    const handleSearch = async (

        value: string
    
    ) => {
    
        setKeyword(value);
    
        if (value === "") {
    
            loadCategories();
    
            return;
    
        }
    
        try {
    
            const response = await searchCategory(value);
    
            setCategories(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const handleOpen = () => {

        setSelectedCategory(null);
    
        setOpen(true);
    
    };
    
    const handleEdit = (
    
        category: any
    
    ) => {
    
        setSelectedCategory(category);
    
        setOpen(true);
    
    };
    
    const handleClose = () => {
    
        setOpen(false);
    
    };

    const handleDelete = async (id: number) => {

        const confirmDelete = window.confirm(
    
            "Are you sure you want to delete this category?"
    
        );
    
        if (!confirmDelete) {
    
            return;
    
        }
    
        try {
    
            await deleteCategory(id);
    
            loadCategories();
    
            alert("Category deleted successfully.");
    
        }
    
        catch (error: any) {
    
            alert(
    
                error.response?.data?.detail ||
    
                "Unable to delete category."
    
            );
    
        }
    
    };

    return (

        <>

            <Sidebar />

            <Navbar />

            <div className="categories">

                <div className="category-header">

                    <h2>Category Management</h2>

                    <input

                        type="text"
                    
                        placeholder="Search Category"
                    
                        value={keyword}
                    
                        onChange={(e) =>
                    
                            handleSearch(e.target.value)
                    
                        }
                    
                    />

                    <button 
                        className="add-btn"
                        
                        onClick={handleOpen}
                    >

                        Add Category

                    </button>

                </div>

                <table>

                    <thead>

                        <tr>

                            <th>ID</th>

                            <th>Name</th>

                            <th>Description</th>

                            <th>Status</th>

                            <th>Total Products</th>

                            <th>Actions</th>

                        </tr>

                    </thead>

                    <tbody>

                        {

                            categories.map((category) => (

                                <tr key={category.id}>

                                    <td>{category.id}</td>

                                    <td>{category.name}</td>

                                    <td>{category.description}</td>

                                    <td>{category.status}</td>

                                    <td>{category.total_products}</td>

                                    <td>

                                        <button
                                        
                                           onClick={() =>
   
                                                handleEdit(category)
                                        
                                            }
                                        
                                        >

                                            Edit

                                        </button>

                                        <button
                                        
                                            onClick={() =>

                                                handleDelete(category.id)
                                        
                                            }

                                        
                                        >

                                            Delete

                                        </button>

                                    </td>

                                </tr>

                            ))

                        }

                    </tbody>

                </table>

            </div>

            <CategoryForm

                open={open}
            
                handleClose={handleClose}
            
                loadCategories={loadCategories}
            
                category={selectedCategory}
            
            />

        </>

    );

}

export default Categories;