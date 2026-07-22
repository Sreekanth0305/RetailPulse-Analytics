import { useState } from "react";

import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    TextField
} from "@mui/material";

import { removeStock } from "../services/inventoryService";

interface Props {

    open: boolean;

    handleClose: () => void;

    inventoryId: number;

    loadInventory: () => void;

}

function RemoveStockForm({

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

            await removeStock(

                inventoryId,

                {

                    quantity: Number(quantity),

                    reason,

                    remarks

                }

            );

            alert("Stock Removed Successfully");

            loadInventory();

            handleClose();

            setQuantity("");

            setReason("");

            setRemarks("");

        }

        catch (error: any) {

            alert(

                error.response?.data?.detail ||

                "Unable to remove stock"

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

                Remove Stock

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

                    color="error"

                    onClick={handleSubmit}

                >

                    Remove

                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default RemoveStockForm;