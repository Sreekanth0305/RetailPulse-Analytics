import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import InventoryForm from "../components/InventoryForm";
import RemoveStockForm from "../components/RemoveStockForm";
import AdjustStockForm from "../components/AdjustStockForm";
import ReorderLevelForm from "../components/ReorderLevelForm";
import InventoryMovementHistory from "../components/InventoryMovementHistory";

import {
    getInventory,
    searchInventory,
    filterInventory,
    sortInventory,
    getCategories
} from "../services/inventoryService";

import "../styles/inventory.css";

interface Inventory {

    id: number;

    product_id: number;

    product_name: string;

    sku: string;

    category: string;

    brand: string;

    current_stock: number;

    reserved_stock: number;

    available_stock: number;

    reorder_level: number;

    stock_status: string;

    updated_at: string;

}

function Inventory() {

    const [inventory, setInventory] = useState<Inventory[]>([]);

    const [keyword, setKeyword] = useState("");

    const [category, setCategory] = useState("");

    const [categories, setCategories] = useState([]);

    const [brand, setBrand] = useState("");

    const [status, setStatus] = useState("");

    const [sortBy, setSortBy] = useState("");

    const [selectedInventory, setSelectedInventory] =
        useState<Inventory | null>(null);

    const [openAddStock, setOpenAddStock] = useState(false);

    const [openRemoveStock, setOpenRemoveStock] = useState(false);

    const [openAdjustStock, setOpenAdjustStock] = useState(false);

    const [openReorderLevel, setOpenReorderLevel] = useState(false);

    const [openMovementHistory, setOpenMovementHistory] = useState(false);

    // ============================
    // Load Inventory
    // ============================

    const loadInventory = async () => {

        try {

            const response = await getInventory();

            setInventory(response.data);

        }

        catch (error) {

            console.log(error);

        }

    };

    const loadCategories = async () => {

    const response = await getCategories();

    setCategories(response.data);

    };

    useEffect(() => {

        loadInventory();

        loadCategories();

    }, []);

    // ============================
    // Search
    // ============================

    const handleSearch = async (value: string) => {

        setKeyword(value);

        if (value.trim() === "") {

            loadInventory();

            return;

        }

        try {

            const response = await searchInventory(value);

            setInventory(response.data);

        }

        catch (error) {

            console.log(error);

        }

    };

    // ============================
    // Filter
    // ============================

    const handleFilter = async () => {

        try {

            const response = await filterInventory(

                category
                    ? Number(category)
                    : undefined,

                brand || undefined,

                status || undefined

            );

            setInventory(response.data);

        }

        catch (error) {

            console.log(error);

        }

    };

    // ============================
    // Sort
    // ============================

    const handleSort = async (value: string) => {

        setSortBy(value);

        if (value === "") {

            loadInventory();

            return;

        }

        try {

            const response = await sortInventory(value);

            setInventory(response.data);

        }

        catch (error) {

            console.log(error);

        }

    };

    // ============================
    // Dialog Handlers
    // ============================

    const handleAddStock = (item: Inventory) => {

        setSelectedInventory(item);

        setOpenAddStock(true);

    };

    const handleRemoveStock = (item: Inventory) => {

        setSelectedInventory(item);

        setOpenRemoveStock(true);

    };

    const handleAdjustStock = (item: Inventory) => {

        setSelectedInventory(item);

        setOpenAdjustStock(true);

    };

    const handleReorderLevel = (item: Inventory) => {

        setSelectedInventory(item);

        setOpenReorderLevel(true);

    };

    const handleMovementHistory = (item: Inventory) => {

        setSelectedInventory(item);

        setOpenMovementHistory(true);

    }; 

        return (

        <>

            <Sidebar />

            <Navbar />

            <div className="inventory">

                <div className="inventory-header">

                    <h2>Inventory Management</h2>

                </div>

                {/* ==========================
                    Toolbar
                =========================== */}

                <div className="inventory-toolbar">

                    <input

                        type="text"

                        placeholder="Search Product / SKU"

                        value={keyword}

                        onChange={(e) =>
                            handleSearch(e.target.value)
                        }

                    />

                    <select
                        value={category}
                        onChange={(e) => setCategory(e.target.value)}
                    >
                    
                        <option value="">
                            Category
                        </option>
                    
                        {categories.map((cat: any) => (
                    
                            <option
                                key={cat.id}
                                value={cat.id}
                            >
                    
                                {cat.name}
                    
                            </option>
                    
                        ))}
                    
                    </select>

                    <input

                        type="text"

                        placeholder="Brand"

                        value={brand}

                        onChange={(e) =>
                            setBrand(e.target.value)
                        }

                    />

                    <select

                        value={status}

                        onChange={(e) =>
                            setStatus(e.target.value)
                        }

                    >

                        <option value="">
                            Stock Status
                        </option>

                        <option value="In Stock">
                            In Stock
                        </option>

                        <option value="Low Stock">
                            Low Stock
                        </option>

                        <option value="Out Of Stock">
                            Out Of Stock
                        </option>

                    </select>

                    <button

                        className="filter-btn"

                        onClick={handleFilter}

                    >

                        Filter

                    </button>

                    <select

                        value={sortBy}

                        onChange={(e) =>
                            handleSort(e.target.value)
                        }

                    >

                        <option value="">
                            Sort By
                        </option>

                        <option value="product">
                            Product Name
                        </option>

                        <option value="stock">
                            Current Stock
                        </option>

                        <option value="updated">
                            Recently Updated
                        </option>

                    </select>

                </div>

                {/* ==========================
                    Inventory Table
                =========================== */}

                <table className="inventory-table">

                    <thead>

                        <tr>

                            <th>Product</th>

                            <th>SKU</th>

                            <th>Category</th>

                            <th>Brand</th>

                            <th>Current Stock</th>

                            <th>Reserved</th>

                            <th>Available</th>

                            <th>Reorder Level</th>

                            <th>Status</th>

                            <th>Actions</th>

                        </tr>

                    </thead>

                    <tbody>

                        {

                            inventory.length > 0 ? (

                                inventory.map((item) => (

                                    <tr key={item.id}>

                                        <td>{item.product_name}</td>

                                        <td>{item.sku}</td>

                                        <td>{item.category}</td>

                                        <td>{item.brand}</td>

                                        <td>{item.current_stock}</td>

                                        <td>{item.reserved_stock}</td>

                                        <td>{item.available_stock}</td>

                                        <td>{item.reorder_level}</td>

                                        <td>

                                            <span

                                                className={`status ${item.stock_status
                                                    .toLowerCase()
                                                    .replace(/\s+/g, "-")}`}

                                            >

                                                {item.stock_status}

                                            </span>

                                        </td>

                                        <td className="inventory-actions">

                                            <button

                                                className="add-btn"

                                                onClick={() =>
                                                    handleAddStock(item)
                                                }

                                            >

                                                Add

                                            </button>

                                            <button

                                                className="remove-btn"

                                                onClick={() =>
                                                    handleRemoveStock(item)
                                                }

                                            >

                                                Remove

                                            </button>

                                            <button

                                                className="adjust-btn"

                                                onClick={() =>
                                                    handleAdjustStock(item)
                                                }

                                            >

                                                Adjust

                                            </button>

                                            <button

                                                className="reorder-btn"

                                                onClick={() =>
                                                    handleReorderLevel(item)
                                                }

                                            >

                                                Reorder

                                            </button>

                                            <button

                                                className="history-btn"

                                                onClick={() =>
                                                    handleMovementHistory(item)
                                                }

                                            >

                                                History

                                            </button>

                                        </td>

                                    </tr>

                                ))

                            ) : (

                                <tr>

                                    <td
                                        colSpan={10}
                                        style={{
                                            textAlign: "center",
                                            padding: "20px"
                                        }}
                                    >

                                        No inventory found.

                                    </td>

                                </tr>

                            )

                        }

                    </tbody>

                </table>

            </div>

        {/* ==========================
            Dialogs
        =========================== */}

        <InventoryForm

            open={openAddStock}

            handleClose={() => {

                setOpenAddStock(false);

                setSelectedInventory(null);

            }}

            inventoryId={selectedInventory?.product_id ?? 0}

            loadInventory={loadInventory}

        />

        <RemoveStockForm

            open={openRemoveStock}

            handleClose={() => {

                setOpenRemoveStock(false);

                setSelectedInventory(null);

            }}

            inventoryId={selectedInventory?.product_id ?? 0}
            loadInventory={loadInventory}

        />

        <AdjustStockForm

            open={openAdjustStock}

            handleClose={() => {

                setOpenAdjustStock(false);

                setSelectedInventory(null);

            }}

            inventoryId={selectedInventory?.product_id ?? 0}

            loadInventory={loadInventory}

        />

        <ReorderLevelForm

            open={openReorderLevel}

            handleClose={() => {

                setOpenReorderLevel(false);

                setSelectedInventory(null);

            }}

            inventoryId={selectedInventory?.product_id ?? 0}

            currentLevel={selectedInventory?.reorder_level ?? 0}

            loadInventory={loadInventory}

        />

        <InventoryMovementHistory

            open={openMovementHistory}

            handleClose={() => {

                setOpenMovementHistory(false);

                setSelectedInventory(null);

            }}

            inventoryId={selectedInventory?.product_id ?? 0}

        />

        </>

    );

}

export default Inventory;