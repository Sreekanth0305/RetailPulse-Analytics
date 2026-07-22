import { useEffect, useState } from "react";

import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    TextField
} from "@mui/material";

import { updateReorderLevel } from "../services/inventoryService";

interface Props {

    open: boolean;

    handleClose: () => void;

    inventoryId: number;

    currentLevel: number;

    loadInventory: () => void;

}

function ReorderLevelForm({

    open,

    handleClose,

    inventoryId,

    currentLevel,

    loadInventory

}: Props) {

    const [reorderLevel, setReorderLevel] =
        useState(0);

    useEffect(() => {

        setReorderLevel(currentLevel);

    }, [currentLevel]);

    const handleSubmit = async () => {

        try {

            await updateReorderLevel(

                inventoryId,

                {

                    reorder_level: Number(reorderLevel)

                }

            );

            alert("Reorder Level Updated Successfully");

            loadInventory();

            handleClose();

        }

        catch (error: any) {

            alert(

                error.response?.data?.detail ||

                "Unable to update reorder level."

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

                Update Reorder Level

            </DialogTitle>

            <DialogContent>

                <TextField

                    fullWidth

                    margin="normal"

                    label="Reorder Level"

                    type="number"

                    value={reorderLevel}

                    onChange={(e)=>

                        setReorderLevel(

                            Number(e.target.value)

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

                    Update

                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default ReorderLevelForm;