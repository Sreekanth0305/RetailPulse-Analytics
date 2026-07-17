import { useEffect, useState } from "react";

import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Button,
    MenuItem
} from "@mui/material";

import { 
    createProduct,
    updateProduct    
 } from "../services/productService";
import { getCategories } from "../services/categoryService";

interface Props {

    open: boolean;

    handleClose: () => void;

    loadProducts: () => void;

    productData?: any;

}

function ProductForm({

    open,

    handleClose,

    loadProducts,

    productData

}: Props) {

    const [categories, setCategories] = useState<any[]>([]);

    const [product, setProduct] = useState({

        category_id: "",

        name: "",

        sku: "",

        brand: "",

        description: "",

        unit_price: "",

        cost_price: "",

        stock_quantity: "",

        unit_of_measure: "Piece",

        status: "Active"

    });

    useEffect(() => {

    loadCategories();

}, []);

useEffect(() => {

    if (productData) {

        setProduct({

            category_id: productData.category_id,

            name: productData.name,

            sku: productData.sku,

            brand: productData.brand,

            description: productData.description,

            unit_price: productData.unit_price,

            cost_price: productData.cost_price,

            stock_quantity: productData.stock_quantity,

            unit_of_measure: productData.unit_of_measure,

            status: productData.status

        });

    }

    else {

        setProduct({

            category_id: "",

            name: "",

            sku: "",

            brand: "",

            description: "",

            unit_price: "",

            cost_price: "",

            stock_quantity: "",

            unit_of_measure: "Piece",

            status: "Active"

        });

    }

}, [productData]);

    const loadCategories = async () => {

        const response = await getCategories();

        setCategories(response.data);

    };

    const handleChange = (

        e: React.ChangeEvent<HTMLInputElement>

    ) => {

        setProduct({

            ...product,

            [e.target.name]: e.target.value

        });

    };

    const handleSave = async () => {

        try {
    
            if (productData) {
    
                await updateProduct(
    
                    productData.id,
    
                    product
    
                );
    
            }
    
            else {
    
                await createProduct(product);
    
            }
    
            loadProducts();
    
            handleClose();
    
        }
    
        catch (error: any) {
    
            alert(
    
                error.response?.data?.detail ||
    
                "Something went wrong."
    
            );
    
        }
    
    };

    return (

        <Dialog
            open={open}
            onClose={handleClose}
            fullWidth
            maxWidth="md"
        >

            <DialogTitle>

                {

                    productData
            
                        ? "Edit Product"
            
                        : "Add Product"
            
                }

            </DialogTitle>

            <DialogContent>

                <TextField
                    fullWidth
                    margin="normal"
                    select
                    label="Category"
                    name="category_id"
                    value={product.category_id}
                    onChange={handleChange}
                >
            
                    {
            
                        categories.map((category) => (
            
                            <MenuItem
                                key={category.id}
                                value={category.id}
                            >
            
                                {category.name}
            
                            </MenuItem>
            
                        ))
            
                    }
            
                </TextField>
            
                <TextField
                    fullWidth
                    margin="normal"
                    label="Product Name"
                    name="name"
                    value={product.name}
                    onChange={handleChange}
                />
            
                <TextField
                    fullWidth
                    margin="normal"
                    label="SKU"
                    name="sku"
                    value={product.sku}
                    onChange={handleChange}
                />
            
                <TextField
                    fullWidth
                    margin="normal"
                    label="Brand"
                    name="brand"
                    value={product.brand}
                    onChange={handleChange}
                />
            
                <TextField
                    fullWidth
                    margin="normal"
                    label="Description"
                    name="description"
                    value={product.description}
                    onChange={handleChange}
                />
            
                <TextField
                    fullWidth
                    margin="normal"
                    type="number"
                    label="Unit Price"
                    name="unit_price"
                    value={product.unit_price}
                    onChange={handleChange}
                />
            
                <TextField
                    fullWidth
                    margin="normal"
                    type="number"
                    label="Cost Price"
                    name="cost_price"
                    value={product.cost_price}
                    onChange={handleChange}
                />
            
                <TextField
                    fullWidth
                    margin="normal"
                    type="number"
                    label="Stock Quantity"
                    name="stock_quantity"
                    value={product.stock_quantity}
                    onChange={handleChange}
                />
            
                <TextField
                    fullWidth
                    margin="normal"
                    label="Unit of Measure"
                    name="unit_of_measure"
                    value={product.unit_of_measure}
                    onChange={handleChange}
                />
            
                <TextField
                    fullWidth
                    margin="normal"
                    select
                    label="Status"
                    name="status"
                    value={product.status}
                    onChange={handleChange}
                >
            
                    <MenuItem value="Active">
            
                        Active
            
                    </MenuItem>
            
                    <MenuItem value="Inactive">
            
                        Inactive
            
                    </MenuItem>
            
                </TextField>
            
            </DialogContent>

            <DialogActions>

                <Button
                    onClick={handleClose}
                >

                    Cancel

                </Button>

                <Button
                    variant="contained"
                    onClick={handleSave}
                >

                    Save

                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default ProductForm;