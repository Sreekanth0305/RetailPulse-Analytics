import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import {
    getProducts,
    deleteProduct,
    searchProduct,
    filterProduct,
    activateProduct,
    deactivateProduct,
    getDashboardSummary,
    sortProduct
} from "../services/productService";

import {

    getCategories

} from "../services/categoryService";

import ProductForm from "../components/ProductForm";

import "../styles/products.css";

function Products() {

    const [products, setProducts] = useState<any[]>([]);

    const [summary, setSummary] = useState({

    total_products: 0,

    active_products: 0,

    inactive_products: 0,

    total_categories: 0

});

    const [open, setOpen] = useState(false);

    const [selectedProduct, setSelectedProduct] = useState<any>(null);
    
    const [search, setSearch] = useState("");

    const [categories, setCategories] = useState<any[]>([]);

    const [categoryFilter, setCategoryFilter] = useState("");
    
    const [brandFilter, setBrandFilter] = useState("");
    
    const [statusFilter, setStatusFilter] = useState("");

    const [sortBy, setSortBy] = useState("");

    const loadProducts = async () => {

        try {

            const response = await getProducts();

            setProducts(response.data);

        }

        catch (error) {

            console.log(error);

        }

    };

    const loadSummary = async () => {

        try {
    
            const response = await getDashboardSummary();
    
            setSummary(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

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

        loadProducts();

        loadCategories();

         loadSummary();

    }, []);


    const handleDelete = async (id: number) => {

        const confirmDelete = window.confirm(
    
            "Are you sure you want to delete this product?"
    
        );
    
        if (!confirmDelete) return;
    
        try {
    
            await deleteProduct(id);
    
            loadProducts();
    
        }
    
        catch (error) {
    
            console.log(error);
    
            alert("Unable to delete product.");
    
        }
    
    };

    const handleActivate = async (

    id: number

) => {

    try {

        await activateProduct(id);

        loadProducts();

    }

    catch (error) {

        console.log(error);

    }

};

const handleDeactivate = async (

    id: number

) => {

    try {

        await deactivateProduct(id);

        loadProducts();

    }

    catch (error) {

        console.log(error);

    }

};

    const handleSearch = async (

        keyword: string
    
    ) => {
    
        setSearch(keyword);
    
        try {
    
            if (keyword.trim() === "") {
    
                loadProducts();
    
                return;
    
            }
    
            const response = await searchProduct(keyword);
    
            setProducts(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const applyFilters = async (

        categoryId: string,
    
        brand: string,
    
        status: string
    
    ) => {
    
        try {
    
            if (
    
                categoryId === "" &&
    
                brand === "" &&
    
                status === ""
    
            ) {
    
                loadProducts();
    
                return;
    
            }
    
            const response = await filterProduct(
    
                categoryId,
    
                brand,
    
                status
    
            );
    
            setProducts(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const handleSort = async (

        value: string
    
    ) => {
    
        setSortBy(value);
    
        try {
    
            if (value === "") {
    
                loadProducts();
    
                return;
    
            }
    
            const response = await sortProduct(value);
    
            setProducts(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    return (

        <>

            <Sidebar />

            <Navbar />

            <div className="products">

                {/* <div className="products-header"> */}

                    <h2>

                        Product Management

                    </h2>

                    <div className="summary-cards">

                        <div className="summary-card">
                    
                            <h3>Total Products</h3>
                    
                            <h2>{summary.total_products}</h2>
                    
                        </div>
                    
                        <div className="summary-card">
                    
                            <h3>Active Products</h3>
                    
                            <h2>{summary.active_products}</h2>
                    
                        </div>
                    
                        <div className="summary-card">
                    
                            <h3>Inactive Products</h3>
                    
                            <h2>{summary.inactive_products}</h2>
                    
                        </div>
                    
                        <div className="summary-card">
                    
                            <h3>Total Categories</h3>
                    
                            <h2>{summary.total_categories}</h2>
                    
                        </div>
                    
                    </div>

                    <div className="products-header"> 

                        <input
    
                            type="text"
                        
                            placeholder="Search by Name, SKU or Brand"
                        
                            value={search}
                        
                            onChange={(e) =>
                        
                                handleSearch(e.target.value)
                        
                            }
                        
                        />
    
                        <select
    
                            value={categoryFilter}
                        
                            onChange={(e) => {
                        
                                setCategoryFilter(e.target.value);
                        
                                applyFilters(
                        
                                    e.target.value,
                        
                                    brandFilter,
                        
                                    statusFilter
                        
                                );
                        
                            }}
                        
                        >
                        
                            <option value="">
                        
                                All Categories
                        
                            </option>
                        
                            {
                        
                                categories.map((category) => (
                        
                                    <option
                        
                                        key={category.id}
                        
                                        value={category.id}
                        
                                    >
                        
                                        {category.name}
                        
                                    </option>
                        
                                ))
                        
                            }
                        
                        </select>
                        
                        <input
                        
                            type="text"
                        
                            placeholder="Brand"
                        
                            value={brandFilter}
                        
                            onChange={(e) => {
                        
                                setBrandFilter(e.target.value);
                        
                                applyFilters(
                        
                                    categoryFilter,
                        
                                    e.target.value,
                        
                                    statusFilter
                        
                                );
                        
                            }}
                        
                        />
                        
                        <select
                        
                            value={statusFilter}
                        
                            onChange={(e) => {
                        
                                setStatusFilter(e.target.value);
                        
                                applyFilters(
                        
                                    categoryFilter,
                        
                                    brandFilter,
                        
                                    e.target.value
                        
                                );
                        
                            }}
                        
                        >
                        
                            <option value="">
                        
                                All Status
                        
                            </option>
                        
                            <option value="Active">
                        
                                Active
                        
                            </option>
                        
                            <option value="Inactive">
                        
                                Inactive
                        
                            </option>
                        
                        </select>

                        <select

                            value={sortBy}
                        
                            onChange={(e) =>
                        
                                handleSort(e.target.value)
                        
                            }
                        
                        >
                        
                            <option value="">
                        
                                Sort By
                        
                            </option>
                        
                            <option value="name">
                        
                                Name
                        
                            </option>
                        
                            <option value="price">
                        
                                Price
                        
                            </option>
                        
                            <option value="recent">
                        
                                Recently Added
                        
                            </option>
                        
                        </select>
    
                        <button 
                            className="add-btn"
                            onClick={() => {
                                
                                setSelectedProduct(null);
                                setOpen(true);
                            }}
                            
                        >
    
                            Add Product
    
                        </button>

                    </div>

                <table>

                    <thead>

                        <tr>

                            <th>ID</th>

                            <th>Name</th>

                            <th>SKU</th>

                            <th>Category</th>

                            <th>Brand</th>

                            <th>Price</th>

                            <th>Stock</th>

                            <th>Status</th>

                            <th>Actions</th>

                        </tr>

                    </thead>

                    <tbody>

                        {

                            products.map((product) => (

                                <tr key={product.id}>

                                    <td>{product.id}</td>

                                    <td>{product.name}</td>

                                    <td>{product.sku}</td>

                                    <td>{product.category_name}</td>

                                    <td>{product.brand}</td>

                                    <td>₹{product.unit_price}</td>

                                    <td>{product.stock_quantity}</td>

                                    <td>{product.status}</td>

                                    <td>

                                        <button
                                    
                                            onClick={() => {
                                    
                                                setSelectedProduct(product);
                                    
                                                setOpen(true);
                                    
                                            }}
                                    
                                        >
                                    
                                            Edit
                                    
                                        </button>
                                    
                                        {
                                    
                                            product.status === "Active"
                                    
                                                ?
                                    
                                                <button
                                    
                                                    onClick={() =>
                                    
                                                        handleDeactivate(product.id)
                                    
                                                    }
                                    
                                                >
                                    
                                                    Deactivate
                                    
                                                </button>
                                    
                                                :
                                    
                                                <button
                                    
                                                    onClick={() =>
                                    
                                                        handleActivate(product.id)
                                    
                                                    }
                                    
                                                >
                                    
                                                    Activate
                                    
                                                </button>
                                    
                                        }
                                    
                                        <button
                                    
                                            onClick={() =>
                                    
                                                handleDelete(product.id)
                                    
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

            <ProductForm

                open={open}
            
                handleClose={() => {
                    
                    setOpen(false);

                    setSelectedProduct(null);

                }}
            
                loadProducts={loadProducts}
                productData={selectedProduct}
            
            />

        </>

    );

}

export default Products;