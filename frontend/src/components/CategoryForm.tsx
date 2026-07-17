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
    createCategory,
    updateCategory
} from "../services/categoryService";

interface Props {

    open: boolean;

    handleClose: () => void;

    loadCategories: () => void;

    category?: any;

}

function CategoryForm({

    open,
    handleClose,
    loadCategories,
    category

}: Props) {

    const [formData, setFormData] = useState({

        name: "",

        description: "",

        status: "Active"

    });

    useEffect(() => {

        if (category) {

            setFormData({

                name: category.name,

                description: category.description,

                status: category.status

            });

        }

        else {

            setFormData({

                name: "",

                description: "",

                status: "Active"

            });

        }

    }, [category]);

    const handleChange = (

        e: React.ChangeEvent<HTMLInputElement>

    ) => {

        setFormData({

            ...formData,

            [e.target.name]: e.target.value

        });

    };

    const handleSubmit = async () => {

        try {

            if (category) {

                await updateCategory(

                    category.id,

                    formData

                );

            }

            else {

                await createCategory(formData);

            }

            loadCategories();

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
            maxWidth="sm"
        >

            <DialogTitle>

                {

                    category

                        ? "Edit Category"

                        : "Add Category"

                }

            </DialogTitle>

            <DialogContent>

                <TextField

                    fullWidth

                    margin="normal"

                    label="Category Name"

                    name="name"

                    value={formData.name}

                    onChange={handleChange}

                />

                <TextField

                    fullWidth

                    margin="normal"

                    label="Description"

                    name="description"

                    value={formData.description}

                    onChange={handleChange}

                />

                <TextField

                    fullWidth

                    margin="normal"

                    select

                    label="Status"

                    name="status"

                    value={formData.status}

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

                    onClick={handleSubmit}

                >

                    Save

                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default CategoryForm;