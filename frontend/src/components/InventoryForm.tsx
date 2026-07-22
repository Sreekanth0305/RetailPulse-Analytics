import { useState } from "react";

import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    TextField
} from "@mui/material";

import { addStock } from "../services/inventoryService";

interface Props {

    open: boolean;

    handleClose: () => void;

    inventoryId: number;

    loadInventory: () => void;

}

function InventoryForm({

    open,

    handleClose,

    inventoryId,

    loadInventory

}: Props) {

    const [quantity, setQuantity] = useState("");

    const [reason, setReason] = useState("");

    const [remarks, setRemarks] = useState("");

    const handleSubmit = async () => {

        try {

            await addStock(

                inventoryId,

                {

                    quantity: Number(quantity),

                    reason,

                    remarks

                }

            );

            alert("Stock Added Successfully");

            loadInventory();

            handleClose();

            setQuantity("");

            setReason("");

            setRemarks("");

        }

        catch (error: any) {

            alert(

                error.response?.data?.detail ||

                "Unable to add stock"

            );

        }

    };

    return (

        <Dialog
            open={open}
            onClose={handleClose}
            fullWidth
        >

            <DialogTitle>

                Add Stock

            </DialogTitle>

            <DialogContent>

                <TextField

                    fullWidth

                    margin="normal"

                    label="Quantity"

                    type="number"

                    value={quantity}

                    onChange={(e)=>

                        setQuantity(e.target.value)

                    }

                />

                <TextField

                    fullWidth

                    margin="normal"

                    label="Reason"

                    value={reason}

                    onChange={(e)=>

                        setReason(e.target.value)

                    }

                />

                <TextField

                    fullWidth

                    margin="normal"

                    label="Remarks"

                    multiline

                    rows={3}

                    value={remarks}

                    onChange={(e)=>

                        setRemarks(e.target.value)

                    }

                />

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

export default InventoryForm;