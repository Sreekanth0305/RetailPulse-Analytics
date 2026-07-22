import { useState } from "react";

import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    TextField,
    MenuItem
} from "@mui/material";

import { adjustStock } from "../services/inventoryService";

interface Props {

    open: boolean;

    handleClose: () => void;

    inventoryId: number;

    loadInventory: () => void;

}

function AdjustStockForm({

    open,

    handleClose,

    inventoryId,

    loadInventory

}: Props) {

    const [movementType, setMovementType] =
        useState("Manual Adjustment");

    const [quantity, setQuantity] =
        useState("");

    const [reason, setReason] =
        useState("");

    const [remarks, setRemarks] =
        useState("");

    const handleSubmit = async () => {

        try {

            await adjustStock(

                inventoryId,

                {

                    movement_type: movementType,

                    quantity: Number(quantity),

                    reason,

                    remarks

                }

            );

            alert("Stock Adjusted Successfully");

            loadInventory();

            handleClose();

            setMovementType(
                "Manual Adjustment"
            );

            setQuantity("");

            setReason("");

            setRemarks("");

        }

        catch (error: any) {

            alert(

                error.response?.data?.detail ||

                "Unable to adjust stock."

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

                Manual Stock Adjustment

            </DialogTitle>

            <DialogContent>

                <TextField

                    select

                    fullWidth

                    margin="normal"

                    label="Adjustment Type"

                    value={movementType}

                    onChange={(e)=>

                        setMovementType(

                            e.target.value

                        )

                    }

                >

                    <MenuItem value="Stock In">

                        Stock In

                    </MenuItem>

                    <MenuItem value="Stock Out">

                        Stock Out

                    </MenuItem>

                    <MenuItem value="Manual Adjustment">

                        Manual Adjustment

                    </MenuItem>

                </TextField>

                <TextField

                    fullWidth

                    margin="normal"

                    label="Quantity"

                    type="number"

                    value={quantity}

                    onChange={(e)=>

                        setQuantity(

                            e.target.value

                        )

                    }

                />

                <TextField

                    fullWidth

                    margin="normal"

                    label="Reason"

                    value={reason}

                    onChange={(e)=>

                        setReason(

                            e.target.value

                        )

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

                        setRemarks(

                            e.target.value

                        )

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

export default AdjustStockForm;