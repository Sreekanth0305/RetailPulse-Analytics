import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import {
    getAnalyticsKPIs,
    getRevenueTrend,
    getSalesTrend,
    getTopSellingProducts,
    getTopCategories,
    getPaymentMethodAnalytics,
    getSalesChannelAnalytics,
    getInventoryDistribution,
    getStockStatusSummary,
    getLowStockProducts,
    getOutOfStockProducts,
    getInventoryValue
} from "../services/analyticsService";

import "../styles/analytics.css";

import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
    BarChart,
    Bar,
    PieChart,
    Pie,
    Cell,
    Legend

} from "recharts";

function Analytics() {

    const [filters, setFilters] = useState({

        start_date: "",

        end_date: "",

        category_id: "",

        product_id: "",

        brand: "",

        sales_channel: "",

        payment_method: ""

    });

    const [kpis, setKpis] = useState({

        total_revenue: 0,
    
        total_orders: 0,
    
        total_products_sold: 0,
    
        average_order_value: 0,
    
        total_inventory_value: 0,
    
        low_stock_products: 0,
    
        out_of_stock_products: 0,
    
        total_categories: 0
    
    });

    const [revenueTrend, setRevenueTrend] = useState<any[]>([]);

    const [revenuePeriod, setRevenuePeriod] = useState("monthly");

    const [salesTrend, setSalesTrend] = useState<any[]>([]);

    const [salesPeriod, setSalesPeriod] = useState("monthly");

    const [topProducts, setTopProducts] = useState<any[]>([]);

    const [topCategories, setTopCategories] = useState<any[]>([]);
    
    const [paymentMethods, setPaymentMethods] = useState<any[]>([]);
    
    const [salesChannels, setSalesChannels] = useState<any[]>([]);
    
    const [inventoryDistribution, setInventoryDistribution] = useState<any[]>([]);
    
    const [inventoryValue, setInventoryValue] = useState<any[]>([]);
    
    const [stockStatus, setStockStatus] = useState<any[]>([]);
    
    const [lowStockProducts, setLowStockProducts] = useState<any[]>([]);
    
    const [outOfStockProducts, setOutOfStockProducts] = useState<any[]>([]);

    const handleFilterChange = (

        e: React.ChangeEvent<
            HTMLInputElement | HTMLSelectElement
        >

    ) => {

        setFilters({

            ...filters,

            [e.target.name]: e.target.value

        });

    };

    const loadKPIs = async () => {

        try {
    
            const params: any = {};
    
            Object.entries(filters).forEach(([key, value]) => {
    
                if (
                    value !== "" &&
                    value !== null &&
                    value !== undefined
                ) {
    
                    params[key] = value;
    
                }
    
            });
    
            const response = await getAnalyticsKPIs(params);
    
            setKpis(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const loadRevenueTrend = async () => {

        try {
    
            const params: any = {
    
                period: revenuePeriod
    
            };
    
            Object.entries(filters).forEach(([key, value]) => {
    
                if (
                    value !== "" &&
                    value !== null &&
                    value !== undefined
                ) {
    
                    params[key] = value;
    
                }
    
            });
    
            const response = await getRevenueTrend(params);
    
            setRevenueTrend(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const loadSalesTrend = async () => {

        try {
    
            const params: any = {
    
                period: salesPeriod
    
            };
    
            Object.entries(filters).forEach(([key, value]) => {
    
                if (
    
                    value !== "" &&
    
                    value !== null &&
    
                    value !== undefined
    
                ) {
    
                    params[key] = value;
    
                }
    
            });
    
            const response = await getSalesTrend(params);
    
            setSalesTrend(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const loadTopProducts = async () => {

        try {
    
            const params: any = {};
    
            Object.entries(filters).forEach(([key, value]) => {
    
                if (
                    value !== "" &&
                    value !== null &&
                    value !== undefined
                ) {
    
                    params[key] = value;
    
                }
    
            });
    
            const response = await getTopSellingProducts(params);
    
            setTopProducts(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const loadTopCategories = async () => {

        try {
    
            const params:any = {};

            Object.entries(filters).forEach(([key,value])=>{
                if(value!=="" && value!==null && value!==undefined){
                    params[key]=value;
                }
            });
            
            const response = await getTopCategories(params);
    
            setTopCategories(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const loadPaymentMethods = async () => {

        try {
    
            const params:any = {};

            Object.entries(filters).forEach(([key,value])=>{
                if(value!=="" && value!==null && value!==undefined){
                    params[key]=value;
                }
            });
            
            const response = await getPaymentMethodAnalytics(params);
            setPaymentMethods(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const loadSalesChannels = async () => {

        try {
    
            const params:any = {};

            Object.entries(filters).forEach(([key,value])=>{
                if(value!=="" && value!==null && value!==undefined){
                    params[key]=value;
                }
            });
            
            const response = await getSalesChannelAnalytics(params);
    
            setSalesChannels(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const loadInventoryDistribution = async () => {

        try {
    
            const params:any = {};

            Object.entries(filters).forEach(([key,value])=>{
                if(value!=="" && value!==null && value!==undefined){
                    params[key]=value;
                }
            });
            
            const response = await getInventoryDistribution(params);
    
            setInventoryDistribution(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const loadInventoryValue = async () => {

        try {
    
            const params:any = {};

            Object.entries(filters).forEach(([key,value])=>{
                if(value!=="" && value!==null && value!==undefined){
                    params[key]=value;
                }
            });
            
            const response = await getInventoryValue(params);
    
            setInventoryValue(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const loadStockStatus = async () => {

        try {
    
            const params:any = {};

            Object.entries(filters).forEach(([key,value])=>{
                if(value!=="" && value!==null && value!==undefined){
                    params[key]=value;
                }
            });

            const response = await getStockStatusSummary(params);
            setStockStatus(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const loadLowStockProducts = async () => {

        try {
    
            const params:any = {};

            Object.entries(filters).forEach(([key,value])=>{
                if(value!=="" && value!==null && value!==undefined){
                    params[key]=value;
                }
            });
            
            const response = await getLowStockProducts(params);
    
            setLowStockProducts(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

        const loadOutOfStockProducts = async () => {
    
        try {
    
            const params:any = {};

            Object.entries(filters).forEach(([key,value])=>{
                if(value!=="" && value!==null && value!==undefined){
                    params[key]=value;
                }
            });
            
            const response = await getOutOfStockProducts(params);
    
            setOutOfStockProducts(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    useEffect(() => {

       loadKPIs();

    }, []);

    useEffect(() => {

       loadRevenueTrend();

    }, [revenuePeriod]);

    useEffect(() => {

       loadSalesTrend();

    }, [salesPeriod]);

    useEffect(() => {

        loadTopProducts();
    
        loadTopCategories();
    
        loadPaymentMethods();
    
        loadSalesChannels();
    
        loadInventoryDistribution();
    
        loadInventoryValue();
    
        loadStockStatus();
    
        loadLowStockProducts();
    
        loadOutOfStockProducts();
    
    }, []);

    return (

        <>

            <Sidebar />

            <Navbar />

            <div className="analytics-page">

                <h1 className="analytics-title">

                    Analytics Dashboard

                </h1>

                <p className="analytics-subtitle">

                    Sales & Inventory Analytics

                </p>

                <div className="filter-panel">

                    <input
                        type="date"
                        name="start_date"
                        value={filters.start_date}
                        onChange={handleFilterChange}
                    />

                    <input
                        type="date"
                        name="end_date"
                        value={filters.end_date}
                        onChange={handleFilterChange}
                    />

                    <input
                        type="text"
                        name="brand"
                        placeholder="Brand"
                        value={filters.brand}
                        onChange={handleFilterChange}
                    />

                    <select
                        name="sales_channel"
                        value={filters.sales_channel}
                        onChange={handleFilterChange}
                    >

                        <option value="">

                            Sales Channel

                        </option>

                        <option value="Retail Store">

                            Retail Store

                        </option>

                        <option value="Online">

                            Online

                        </option>

                        <option value="Marketplace">

                            Marketplace

                        </option>

                    </select>

                    <select
                        name="payment_method"
                        value={filters.payment_method}
                        onChange={handleFilterChange}
                    >

                        <option value="">

                            Payment Method

                        </option>

                        <option value="Cash">

                            Cash

                        </option>

                        <option value="Card">

                            Card

                        </option>

                        <option value="UPI">

                            UPI

                        </option>

                    </select>

                    <button 
                        onClick={ () => {
                            loadKPIs();
                            loadRevenueTrend();
                            loadSalesTrend();
                            loadTopProducts();
                            loadTopCategories();
                            loadPaymentMethods();
                            loadSalesChannels();
                            loadInventoryDistribution();
                            loadInventoryValue();
                            loadStockStatus();
                            loadLowStockProducts();
                            loadOutOfStockProducts();
                        }}
                    >

                        Apply Filters
                    
                    </button>

                </div>

                <h2 className="section-title">

                    Dashboard KPIs
                
                </h2>
                
                <div className="cards">
                
                    <div className="card">
                
                        <h3>Total Revenue</h3>
                
                        <h1>
                
                            ₹{Number(kpis.total_revenue).toLocaleString()}
                
                        </h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Total Orders</h3>
                
                        <h1>
                
                            {kpis.total_orders}
                
                        </h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Products Sold</h3>
                
                        <h1>
                
                            {kpis.total_products_sold}
                
                        </h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Average Order Value</h3>
                
                        <h1>
                
                            ₹{Number(kpis.average_order_value).toFixed(2)}
                
                        </h1>
                
                    </div>
                
                </div>
                
                <div className="cards">
                
                    <div className="card">
                
                        <h3>Inventory Value</h3>
                
                        <h1>
                
                            ₹{Number(kpis.total_inventory_value).toLocaleString()}
                
                        </h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Low Stock</h3>
                
                        <h1>
                
                            {kpis.low_stock_products}
                
                        </h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Out Of Stock</h3>
                
                        <h1>
                
                            {kpis.out_of_stock_products}
                
                        </h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Total Categories</h3>
                
                        <h1>
                
                            {kpis.total_categories}
                
                        </h1>
                
                    </div>
                
                </div>

                <h2 className="section-title">

                    Revenue Trend
                
                </h2>
                
                <div className="chart-card">
                
                    <div className="chart-header">
                
                        <select
                
                            value={revenuePeriod}
                
                            onChange={(e) => {
                
                                setRevenuePeriod(e.target.value)
                
                            }}
                
                        >
                
                            <option value="daily">
                
                                Daily
                
                            </option>
                
                            <option value="weekly">
                
                                Weekly
                
                            </option>
                
                            <option value="monthly">
                
                                Monthly
                
                            </option>
                
                        </select>
                
                    </div>
                
                    <ResponsiveContainer
                
                        width="100%"
                
                        height={350}
                
                    >
                
                        <LineChart
                
                            data={revenueTrend}
                
                        >
                
                            <CartesianGrid strokeDasharray="3 3" />
                
                            <XAxis dataKey="period" />
                
                            <YAxis />
                
                            <Tooltip />
                
                            <Line
                
                                type="monotone"
                
                                dataKey="revenue"
                
                                stroke="#1976d2"
                
                                strokeWidth={3}
                
                            />
                
                        </LineChart>
                
                    </ResponsiveContainer>
                
                </div>

                <h2 className="section-title">

                    Sales Trend
                
                </h2>
                
                <div className="chart-card">
                
                    <div className="chart-header">
                
                        <select
                
                            value={salesPeriod}
                
                            onChange={(e) => {
                
                                setSalesPeriod(e.target.value)
                
                            }}
                
                        >
                
                            <option value="daily">
                
                                Daily
                
                            </option>
                
                            <option value="weekly">
                
                                Weekly
                
                            </option>
                
                            <option value="monthly">
                
                                Monthly
                
                            </option>
                
                        </select>
                
                    </div>
                
                    <ResponsiveContainer
                
                        width="100%"
                
                        height={350}
                
                    >
                
                        <LineChart
                
                            data={salesTrend}
                
                        >
                
                            <CartesianGrid strokeDasharray="3 3" />
                
                            <XAxis dataKey="period" />
                
                            <YAxis />
                
                            <Tooltip />
                
                            <Line
                
                                type="monotone"
                
                                dataKey="orders"
                
                                stroke="#2e7d32"
                
                                strokeWidth={3}
                
                            />
                
                        </LineChart>
                
                    </ResponsiveContainer>
                
                </div>

                <h2 className="section-title">
                    Sales Analytics
                </h2>
                
                <div className="analytics-grid">
                
                    <div className="chart-card">
                
                        <h3>Top 10 Best Selling Products</h3>
                
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={topProducts}>

                                <CartesianGrid strokeDasharray="3 3" />
                            
                                <XAxis dataKey="product_name" />
                            
                                <YAxis />
                            
                                <Tooltip />
                            
                                <Bar
                                    dataKey="quantity_sold"
                                    fill="#1976d2"
                                />
                            
                            </BarChart>
                        </ResponsiveContainer>
                
                    </div>
                
                    <div className="chart-card">
                
                        <h3>Top Performing Categories</h3>
                
                        <ResponsiveContainer width="100%" height={300}>
                            <PieChart>

                                <Pie
                            
                                    data={topCategories}
                            
                                    dataKey="quantity_sold"
                            
                                    nameKey="category_name"
                            
                                    outerRadius={90}
                            
                                    label
                            
                                >
                            
                                    {
                                        topCategories.map((_, index) => (
                            
                                            <Cell
                                                key={index}
                                            />
                            
                                        ))
                                    }
                            
                                </Pie>
                            
                                <Tooltip />
                            
                                <Legend />
                            
                            </PieChart>
                        </ResponsiveContainer>
                
                    </div>
                
                </div>

                <div className="analytics-grid">

                    <div className="chart-card">
                
                        <h3>Sales By Payment Method</h3>
                
                        <ResponsiveContainer width="100%" height={300}>
                            <PieChart>

                                <Pie
                            
                                    data={paymentMethods}
                            
                                    dataKey="total_sales"
                            
                                    nameKey="payment_method"
                            
                                    outerRadius={90}
                            
                                    label
                            
                                >
                            
                                    {
                                        paymentMethods.map((_, index) => (
                            
                                            <Cell
                                                key={index}
                                            />
                            
                                        ))
                                    }
                            
                                </Pie>
                            
                                <Tooltip />
                            
                                <Legend />
                            
                            </PieChart>
                        </ResponsiveContainer>
                
                    </div>
                
                    <div className="chart-card">
                
                        <h3>Sales By Sales Channel</h3>
                
                        <ResponsiveContainer width="100%" height={300}>
                            <PieChart>

                                <Pie
                            
                                    data={salesChannels}
                            
                                    dataKey="total_sales"
                            
                                    nameKey="sales_channel"
                            
                                    outerRadius={90}
                            
                                    label
                            
                                >
                            
                                    {
                                        salesChannels.map((_, index) => (
                            
                                            <Cell
                                                key={index}
                                            />
                            
                                        ))
                                    }
                            
                                </Pie>
                            
                                <Tooltip />
                            
                                <Legend />
                            
                            </PieChart>
                        </ResponsiveContainer>
                
                    </div>
                
                </div>

                <h2 className="section-title">
                    Inventory Analytics
                </h2>
                
                <div className="analytics-grid">
                
                    <div className="chart-card">
                
                        <h3>Inventory Distribution</h3>
                
                        <ResponsiveContainer width="100%" height={300}>
                            <PieChart>

                                <Pie
                            
                                    data={inventoryDistribution}
                            
                                    dataKey="current_stock"
                            
                                    nameKey="category_name"
                            
                                    outerRadius={90}
                            
                                    label
                            
                                >
                            
                                    {
                                        inventoryDistribution.map((_, index) => (
                            
                                            <Cell
                                                key={index}
                                            />
                            
                                        ))
                                    }
                            
                                </Pie>
                            
                                <Tooltip />
                            
                                <Legend />
                            
                            </PieChart>
                        </ResponsiveContainer>
                
                    </div>
                
                    <div className="chart-card">
                
                        <h3>Inventory Value By Category</h3>
                
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={inventoryValue}>

                                <CartesianGrid strokeDasharray="3 3" />
                            
                                <XAxis dataKey="category_name" />
                            
                                <YAxis />
                            
                                <Tooltip />
                            
                                <Bar
                            
                                    dataKey="inventory_value"
                            
                                    fill="#4caf50"
                            
                                />
                            
                            </BarChart>
                        </ResponsiveContainer>
                
                    </div>
                
                </div>

                <div className="analytics-grid">

                    <div className="chart-card">
                
                        <h3>Stock Status Summary</h3>
                
                        <ResponsiveContainer width="100%" height={300}>
                            <PieChart>

                                <Pie
                            
                                    data={stockStatus}
                            
                                    dataKey="total_products"
                            
                                    nameKey="stock_status"
                            
                                    outerRadius={90}
                            
                                    label
                            
                                >
                            
                                    {
                                        stockStatus.map((_, index) => (
                            
                                            <Cell
                                                key={index}
                                            />
                            
                                        ))
                                    }
                            
                                </Pie>
                            
                                <Tooltip />
                            
                                <Legend />
                            
                            </PieChart>
                        </ResponsiveContainer>
                
                    </div>
                
                    <div className="chart-card">
                
                        <h3>Top Low Stock Products</h3>
                
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={lowStockProducts}>

                                <CartesianGrid strokeDasharray="3 3" />
                            
                                <XAxis dataKey="product_name" />
                            
                                <YAxis />
                            
                                <Tooltip />
                            
                                <Bar
                            
                                    dataKey="current_stock"
                            
                                    fill="#ff9800"
                            
                                />
                            
                            </BarChart>
                        </ResponsiveContainer>
                
                    </div>
                
                </div>

                <div className="chart-card">

                    <h3>Out Of Stock Products</h3>
                
                    <table className="analytics-table">
                
                        <thead>
                
                            <tr>
                
                                <th>Product</th>
                
                                <th>Category</th>
                
                                <th>Brand</th>
                
                                <th>Stock</th>
                
                            </tr>
                
                        </thead>
                
                        <tbody>
                        {
                            outOfStockProducts.map((item: any, index: number) => (
                                <tr key={index}>
                                    <td>{item.product_name}</td>
                                    <td>-</td>
                                    <td>-</td>
                                    <td>{item.current_stock}</td>
                                </tr>
                            ))
                        }
                        </tbody>
                
                    </table>
                
                </div>

            </div>

        </>

    );

}

export default Analytics;