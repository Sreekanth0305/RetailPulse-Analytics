import { useEffect, useState } from "react";

import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    Table,
    TableHead,
    TableRow,
    TableCell,
    TableBody
} from "@mui/material";

import { getInventoryMovements } from "../services/inventoryService";

interface Props {

    open: boolean;

    handleClose: () => void;

    inventoryId: number;

}

function InventoryMovementHistory({

    open,

    handleClose,

    inventoryId

}: Props) {

    const [movements, setMovements] = useState<any[]>([]);

    const loadHistory = async () => {

        try {

            const response = await getInventoryMovements(
                inventoryId
            );

            setMovements(response.data);

        }

        catch (error) {

            console.log(error);

        }

    };

    useEffect(() => {

        if (open) {

            loadHistory();

        }

    }, [open]);

    return (

        <Dialog

            open={open}

            onClose={handleClose}

            fullWidth

            maxWidth="lg"

        >

            <DialogTitle>

                Inventory Movement History

            </DialogTitle>

            <DialogContent>

                <Table>

                    <TableHead>

                        <TableRow>

                            <TableCell>
                                Product
                            </TableCell>

                            <TableCell>
                                Movement
                            </TableCell>

                            <TableCell>
                                Previous Qty
                            </TableCell>

                            <TableCell>
                                Updated Qty
                            </TableCell>

                            <TableCell>
                                Changed
                            </TableCell>

                            <TableCell>
                                Reason
                            </TableCell>

                            <TableCell>
                                Remarks
                            </TableCell>

                            <TableCell>
                                Performed By
                            </TableCell>

                            <TableCell>
                                Date
                            </TableCell>

                        </TableRow>

                    </TableHead>

                    <TableBody>

                        {

                            movements.map((movement) => (

                                <TableRow key={movement.id}>

                                    <TableCell>

                                        {movement.product_name}

                                    </TableCell>

                                    <TableCell>

                                        {movement.movement_type}

                                    </TableCell>

                                    <TableCell>

                                        {movement.previous_quantity}

                                    </TableCell>

                                    <TableCell>

                                        {movement.updated_quantity}

                                    </TableCell>

                                    <TableCell>

                                        {movement.quantity_changed}

                                    </TableCell>

                                    <TableCell>

                                        {movement.reason}

                                    </TableCell>

                                    <TableCell>

                                        {movement.remarks}

                                    </TableCell>

                                    <TableCell>

                                        {movement.performed_by}

                                    </TableCell>

                                    <TableCell>

                                        {

                                            new Date(

                                                movement.created_at

                                            ).toLocaleString()

                                        }

                                    </TableCell>

                                </TableRow>

                            ))

                        }

                    </TableBody>

                </Table>

            </DialogContent>

            <DialogActions>

                <Button

                    onClick={handleClose}

                >

                    Close

                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default InventoryMovementHistory;