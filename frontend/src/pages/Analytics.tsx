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
    getInventoryValue,
    getDrilldownCategories,
    getDrilldownProducts,
    getDrilldownSales,
    getForecastDashboard,
    getHistoricalVsForecast,
    getProductDemandTrend,
    getCategoryDemandTrend,
    getTopPredictedProducts,
    getSeasonalSalesPattern,
    getTopCustomers

} from "../services/analyticsService";

import { getCustomerAnalytics } from "../services/customerService";

import { createAuditLog } from "../services/auditService";

import "../styles/analytics.css";

import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

import {
    ResponsiveContainer,
    LineChart,
    Line,
    ScatterChart,
    Scatter,
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

        total_discount: 0,

        total_tax: 0,
    
        total_inventory_value: 0,
    
        low_stock_products: 0,
    
        out_of_stock_products: 0,
    
        total_categories: 0
    
    });

    const [revenueTrend, setRevenueTrend] = useState<any[]>([]);

    const [revenuePeriod, setRevenuePeriod] = useState("monthly");

    const [salesTrend, setSalesTrend] = useState<any[]>([]);

    const [salesPeriod, setSalesPeriod] = useState("monthly");

    const [salesVsOrdersPeriod, setSalesVsOrdersPeriod] =
    useState("monthly");

    const [salesVsOrdersData, setSalesVsOrdersData] =
    useState<any[]>([]);

    const [topProducts, setTopProducts] = useState<any[]>([]);

    const [topCategories, setTopCategories] = useState<any[]>([]);
    
    const [paymentMethods, setPaymentMethods] = useState<any[]>([]);
    
    const [salesChannels, setSalesChannels] = useState<any[]>([]);
    
    const [inventoryDistribution, setInventoryDistribution] = useState<any[]>([]);
    
    const [inventoryValue, setInventoryValue] = useState<any[]>([]);
    
    const [stockStatus, setStockStatus] = useState<any[]>([]);
    
    const [lowStockProducts, setLowStockProducts] = useState<any[]>([]);
    
    const [outOfStockProducts, setOutOfStockProducts] = useState<any[]>([]);

    const [categories,setCategories] = useState([]);

    const [products,setProducts] = useState([]);
    
    const [sales,setSales] = useState([]);
    
    const [selectedCategory, setSelectedCategory] = useState<number | null>(null);

    const [selectedProduct, setSelectedProduct] = useState<number | null>(null);

    const [refreshing, setRefreshing] = useState(false);

    const [customerAnalytics, setCustomerAnalytics] = useState<any>(null);

    const [topCustomers, setTopCustomers] = useState<any[]>([]);

    const [productSort, setProductSort] = useState<
        "quantity" | "revenue"
    >("quantity");
    
    const [datePreset, setDatePreset] = useState("custom");
    
    const [analyticsLoading, setAnalyticsLoading] = useState(false);
    
    const [analyticsError, setAnalyticsError] = useState("");
    
    const [customerFilter, setCustomerFilter] = useState("");

    const [forecastDashboard, setForecastDashboard] = useState<any>(null);

    const [historicalForecast, setHistoricalForecast] = useState<any[]>([]);

    const [productTrend, setProductTrend] = useState<any[]>([]);
    
    const [categoryTrend, setCategoryTrend] = useState<any[]>([]);
    
    const [topForecastProducts, setTopForecastProducts] = useState<any[]>([]);
    
    const [seasonalPattern, setSeasonalPattern] = useState<any[]>([]);

    const getBrowser = () => {
        return navigator.userAgent;
    };

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

    const applyDatePreset = (preset: string) => {

        const today = new Date();
    
        const formatDate = (date: Date) => {
            return date.toISOString().split("T")[0];
        };
    
        let start = "";
        let end = formatDate(today);
    
        if (preset === "today") {
    
            start = formatDate(today);
    
        }
    
        else if (preset === "last7") {
    
            const date = new Date(today);
            date.setDate(date.getDate() - 6);
    
            start = formatDate(date);
    
        }
    
        else if (preset === "last30") {
    
            const date = new Date(today);
            date.setDate(date.getDate() - 29);
    
            start = formatDate(date);
    
        }
    
        else if (preset === "thisMonth") {
    
            const date = new Date(
                today.getFullYear(),
                today.getMonth(),
                1
            );
    
            start = formatDate(date);
    
        }
    
        else if (preset === "lastMonth") {
    
            const startDate = new Date(
                today.getFullYear(),
                today.getMonth() - 1,
                1
            );
    
            const endDate = new Date(
                today.getFullYear(),
                today.getMonth(),
                0
            );
    
            start = formatDate(startDate);
            end = formatDate(endDate);
    
        }
    
        setDatePreset(preset);
    
        setFilters(prev => ({
            ...prev,
            start_date: start,
            end_date: end
        }));
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

            if (customerFilter !== "") {
                params.customer_name = customerFilter;
            }
    
            const response = await getAnalyticsKPIs(params);
    
            setKpis(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const loadCustomerAnalytics = async () => {

        try {
    
            const response = await getCustomerAnalytics();
    
            setCustomerAnalytics(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const loadTopCustomers = async () => {

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
    
            if (customerFilter !== "") {
    
                params.customer_name = customerFilter;
    
            }
    
            const response = await getTopCustomers(params);
    
            setTopCustomers(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const loadForecastDashboard = async () => {

        try {
    
            const response = await getForecastDashboard();
    
            setForecastDashboard(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    const loadHistoricalForecast = async () => {

        const response = await getHistoricalVsForecast();
    
        setHistoricalForecast(response.data);
    
    };
    
    const loadProductTrend = async () => {
    
        const response = await getProductDemandTrend();
    
        setProductTrend(response.data);
    
    };
    
    const loadCategoryTrend = async () => {
    
        const response = await getCategoryDemandTrend();
    
        setCategoryTrend(response.data);
    
    };
    
    const loadTopForecastProducts = async () => {
    
        const response = await getTopPredictedProducts();
    
        setTopForecastProducts(response.data);
    
    };
    
    const loadSeasonalPattern = async () => {
    
        const response = await getSeasonalSalesPattern();
    
        setSeasonalPattern(response.data);
    
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

            if (customerFilter !== "") {
                params.customer_name = customerFilter;
            }
    
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

            if (customerFilter !== "") {
                params.customer_name = customerFilter;
            }
    
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

            params.sort_by = productSort;

            if (customerFilter !== "") {
                params.customer_name = customerFilter;
            }
    
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

            if (customerFilter !== "") {
                params.customer_name = customerFilter;
            }
            
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

    const refreshDashboard = async () => {

        setRefreshing(true);
        setAnalyticsLoading(true);
        setAnalyticsError("");
    
        try {
    
            await Promise.all([
                loadKPIs(),
                loadRevenueTrend(),
                loadSalesTrend(),
                loadTopProducts(),
                loadTopCategories(),
                loadPaymentMethods(),
                loadSalesChannels(),
                loadInventoryDistribution(),
                loadInventoryValue(),
                loadStockStatus(),
                loadLowStockProducts(),
                loadOutOfStockProducts(),
                loadCustomerAnalytics(),
                loadTopCustomers(),
                loadForecastDashboard(),
                loadHistoricalForecast(),
                loadProductTrend(),
                loadCategoryTrend(),
                loadTopForecastProducts(),
                loadSeasonalPattern(),
                loadCategories()
            ]);
    
        } catch (error) {
    
            console.error(error);
    
            setAnalyticsError(
                "Unable to load analytics data."
            );
    
        } finally {
    
            setRefreshing(false);
            setAnalyticsLoading(false);
    
        }
    
    };

    const exportCSV = () => {

        let csv = "";
    
        csv += "Dashboard KPIs\n";
        csv += "Metric,Value\n";
        csv += `Total Revenue,${kpis.total_revenue}\n`;
        csv += `Total Orders,${kpis.total_orders}\n`;
        csv += `Products Sold,${kpis.total_products_sold}\n`;
        csv += `Average Order Value,${kpis.average_order_value}\n`;
        csv += `Inventory Value,${kpis.total_inventory_value}\n`;
        csv += `Low Stock,${kpis.low_stock_products}\n`;
        csv += `Out Of Stock,${kpis.out_of_stock_products}\n`;
        csv += `Categories,${kpis.total_categories}\n\n`;
    
        csv += "Revenue Trend\n";
        csv += "Period,Revenue\n";
    
        revenueTrend.forEach((item:any) => {
    
            csv += `${item.period},${item.revenue}\n`;
    
        });
    
        csv += "\nTop Selling Products\n";
        csv += "Product,Quantity Sold\n";
    
        topProducts.forEach((item:any) => {
    
            csv += `${item.product_name},${item.quantity_sold}\n`;
    
        });
    
        csv += "\nSales History\n";
        csv += "Invoice,Customer,Date,Quantity,Amount,Payment,Channel\n";
    
        sales.forEach((item:any) => {
    
            csv += `${item.invoice_number},${item.customer_name},${item.sale_date},${item.quantity},${item.total_amount},${item.payment_method},${item.sales_channel}\n`;
    
        });
    
        const blob = new Blob([csv], {
    
            type: "text/csv;charset=utf-8;"
    
        });
    
        const url = URL.createObjectURL(blob);
    
        const link = document.createElement("a");
    
        link.href = url;
    
        link.download = "Analytics_Report.csv";
    
        link.click();

        createAuditLog({
            action: "Report Exported",
            module: "Analytics",
            export_type: "CSV",
            browser: getBrowser()
        });
    
    };

    const exportPDF = () => {

        const doc = new jsPDF();
    
        doc.setFontSize(18);
    
        doc.text("RetailPulse Analytics Report", 14, 15);
    
        autoTable(doc, {
    
            startY: 25,
    
            head: [["Metric", "Value"]],
    
            body: [
    
                ["Total Revenue", kpis.total_revenue],
    
                ["Total Orders", kpis.total_orders],
    
                ["Products Sold", kpis.total_products_sold],
    
                ["Average Order Value", kpis.average_order_value],
    
                ["Inventory Value", kpis.total_inventory_value],
    
                ["Low Stock", kpis.low_stock_products],
    
                ["Out Of Stock", kpis.out_of_stock_products],
    
                ["Categories", kpis.total_categories]
    
            ]
    
        });
    
        autoTable(doc, {
    
            startY: (doc as any).lastAutoTable.finalY + 10,
    
            head: [["Product", "Quantity Sold"]],
    
            body: topProducts.map((item:any) => [
    
                item.product_name,
    
                item.quantity_sold
    
            ])
    
        });
    
        autoTable(doc, {
    
            startY: (doc as any).lastAutoTable.finalY + 10,
    
            head: [[
    
                "Invoice",
    
                "Customer",
    
                "Date",
    
                "Qty",
    
                "Amount"
    
            ]],
    
            body: sales.map((sale:any) => [
    
                sale.invoice_number,
    
                sale.customer_name,
    
                sale.sale_date,
    
                sale.quantity,
    
                sale.total_amount
    
            ])
    
        });
    
        doc.save("Analytics_Report.pdf");

        createAuditLog({
            action: "Report Exported",
            module: "Analytics",
            export_type: "PDF",
            browser: getBrowser()
        });

    
    };

    const loadCategories = async () => {

        try {
    
            const res = await getDrilldownCategories();
    
            setCategories(res.data);
    
        }
    
        catch (err) {
    
            console.log(err);
    
        }
    
    };

    const loadSalesVsOrders = async () => {

        try {

            const response = await getSalesTrend({
                period: salesVsOrdersPeriod
            });

            setSalesVsOrdersData(response.data);

        } catch (error) {

            console.error(
                "Failed to load Sales vs Orders data:",
                error
            );

        }

    };
    
    const loadProducts = async (categoryId:number) => {
    
        try {
    
            const res = await getDrilldownProducts(categoryId);
    
            setProducts(res.data);
    
            setSelectedCategory(categoryId);
    
            setSales([]);
    
        }
    
        catch (err) {
    
            console.log(err);
    
        }
    
    };
    
    const loadSales = async (productId:number) => {
    
        try {

            console.log("Selected Product:", productId);
    
            const res = await getDrilldownSales(productId);

            console.log("Sales API Response:", res.data);
    
            setSales(res.data);
    
            setSelectedProduct(productId);
    
        }
    
        catch (err) {
    
            console.log(err);
    
        }
    
    };

    useEffect(() => {

        refreshDashboard();
    
        createAuditLog({
            action: "Dashboard Viewed",
            module: "Analytics",
            browser: getBrowser()
        });
    
    }, []);

    useEffect(() => {

       loadRevenueTrend();

    }, [revenuePeriod]);

    useEffect(() => {

       loadSalesTrend();

    }, [salesPeriod]);

    useEffect(() => {

        loadTopProducts();
    
    }, [productSort]);

    useEffect(() => {

        loadCategories();
    
    }, []);

    useEffect(() => {

        loadSalesVsOrders();
    
    }, [salesVsOrdersPeriod]);

    useEffect(() => {

        const interval = setInterval(() => {
    
            refreshDashboard();
    
        }, 30000);
    
        return () => clearInterval(interval);
    
    }, []);

    return (

        <>

            <Sidebar />

            <Navbar />

            <div className="analytics-page">

                {analyticsLoading && (
                    <div className="analytics-loading">
                        Loading analytics dashboard...
                    </div>
                )}
            
                {analyticsError && (
                    <div className="analytics-error">
                        {analyticsError}
                    </div>
                )}


                <h1 className="analytics-title">

                    Analytics Dashboard

                </h1>

                <p className="analytics-subtitle">

                    Sales & Inventory Analytics

                </p>
                <div className="analytics-header-actions">
                    <button
                        className="refresh-btn"
                        onClick={refreshDashboard}
                        disabled={refreshing}
                    >
                        {refreshing ? "Refreshing..." : "Refresh Dashboard"}
                    </button>
                </div>

                <div className="filter-panel">

                    <select
                        value={datePreset}
                        onChange={(e) => applyDatePreset(e.target.value)}
                    >
                        <option value="custom">Custom Date</option>
                        <option value="today">Today</option>
                        <option value="last7">Last 7 Days</option>
                        <option value="last30">Last 30 Days</option>
                        <option value="thisMonth">This Month</option>
                        <option value="lastMonth">Last Month</option>
                    </select>

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

                    <input
                        type="text"
                        placeholder="Customer Name"
                        value={customerFilter}
                        onChange={(e) => setCustomerFilter(e.target.value)}
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
                            loadTopCustomers();

                            createAuditLog({
                                action: "Dashboard Filters Applied",
                                module: "Analytics",
                                browser: getBrowser()
                            });

                        }}
                    >

                        Apply Filters
                    
                    </button>

                    {/* <div className="refresh-container">
                        <button
                            className="refresh-btn"
                            onClick={refreshDashboard}
                            disabled={refreshing}
                        >
                            {refreshing ? "Refreshing..." : "Refresh Dashboard"}
                        </button>
                    </div> */}

                    <button onClick={exportCSV}>
                        Export CSV
                    </button>
                    
                    <button onClick={exportPDF}>
                        Export PDF
                    </button>

                </div>

                <h2 className="section-title">
                    Dashboard KPIs
                </h2>
                
                <div className="cards">
                
                    <div className="card">
                        <h3>Total Revenue</h3>
                        <h1>
                            ₹{Number(kpis.total_revenue ?? 0).toLocaleString("en-IN", {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2
                            })}
                        </h1>
                    </div>
                
                    <div className="card">
                        <h3>Total Orders</h3>
                        <h1>
                            {Number(kpis.total_orders ?? 0).toLocaleString("en-IN")}
                        </h1>
                    </div>
                
                    <div className="card">
                        <h3>Average Order Value</h3>
                        <h1>
                            ₹{Number(kpis.average_order_value ?? 0).toLocaleString("en-IN", {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2
                            })}
                        </h1>
                    </div>
                
                    <div className="card">
                        <h3>Total Items Sold</h3>
                        <h1>
                            {Number(kpis.total_products_sold ?? 0).toLocaleString("en-IN")}
                        </h1>
                    </div>
                
                    <div className="card">
                        <h3>Total Discount</h3>
                        <h1>
                            ₹{Number(kpis.total_discount ?? 0).toLocaleString("en-IN", {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2
                            })}
                        </h1>
                    </div>
                
                    <div className="card">
                        <h3>Total Tax</h3>
                        <h1>
                            ₹{Number(kpis.total_tax ?? 0).toLocaleString("en-IN", {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2
                            })}
                        </h1>
                    </div>
                
                </div>

                <h2 className="section-title">
                    Forecast Dashboard
                </h2>
                
                <div className="cards">
                
                    <div className="card">
                        <h3>Total Predicted Demand</h3>
                        <h1>
                            {forecastDashboard?.total_predicted_demand ?? 0}
                        </h1>
                    </div>
                
                    <div className="card">
                        <h3>Products Expected To Run Out</h3>
                        <h1>
                            {forecastDashboard?.products_expected_to_run_out ?? 0}
                        </h1>
                    </div>
                
                    <div className="card">
                        <h3>High Growth Products</h3>
                        <h1>
                            {forecastDashboard?.high_growth_products ?? 0}
                        </h1>
                    </div>
                
                    <div className="card">
                        <h3>Slow Moving Products</h3>
                        <h1>
                            {forecastDashboard?.slow_moving_products ?? 0}
                        </h1>
                    </div>
                
                    <div className="card">
                        <h3>Forecast Accuracy</h3>
                        <h1>
                            {forecastDashboard?.forecast_accuracy ?? 0}%
                        </h1>
                    </div>
                
                </div>

                <h2 className="section-title">

                    Inventory Analytics
                
                </h2>
                
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

                    Customer Analytics
                
                </h2>
                
                <div className="cards">
                
                    <div className="card">
                
                        <h3>Total Customers</h3>
                
                        <h1>{customerAnalytics?.total_customers ?? 0}</h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Active Customers</h3>
                
                        <h1>{customerAnalytics?.active_customers ?? 0}</h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>New Customers</h3>
                
                        <h1>{customerAnalytics?.new_customers ?? 0}</h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Returning Customers</h3>
                
                        <h1>{customerAnalytics?.returning_customers ?? 0}</h1>
                
                    </div>
                
                </div>
                
                <div className="cards">
                
                    <div className="card">
                
                        <h3>Average Customer Spend</h3>
                
                        <h1>
                
                            ₹{customerAnalytics?.average_customer_spend ?? 0}
                
                        </h1>
                
                    </div>

                    <div className="card">

                        <h3>Customer Average Order Value</h3>
                    
                        <h1>
                            ₹{customerAnalytics?.average_order_value ?? 0}
                        </h1>
                    
                    </div>
                
                    <div className="card">
                
                        <h3>Total Customer Revenue</h3>
                
                        <h1>
                
                            ₹{customerAnalytics?.total_revenue ?? 0}
                
                        </h1>
                
                    </div>
                
                    <div className="card">
                
                        <h3>Purchase Frequency</h3>
                
                        <h1>
                
                            {customerAnalytics?.purchase_frequency ?? 0}
                
                        </h1>
                
                    </div>
                
                </div>

                <h2 className="section-title">

                    Customer Charts
                
                </h2>
                
                <div className="analytics-grid">
                
                    <div className="chart-card">
                
                        <h3>Customer Growth</h3>
                
                        <ResponsiveContainer width="100%" height={300}>
                
                            <LineChart data={customerAnalytics?.customer_growth ?? []}>
                
                                <CartesianGrid strokeDasharray="3 3"/>
                
                                <XAxis dataKey="month"/>
                
                                <YAxis/>
                
                                <Tooltip/>
                
                                <Line
                
                                    type="monotone"
                
                                    dataKey="customers"
                
                                    stroke="#1976d2"
                
                                    strokeWidth={3}
                
                                />
                
                            </LineChart>
                
                        </ResponsiveContainer>
                
                    </div>
                
                    <div className="chart-card">
                
                        <h3>Revenue by Customer Type</h3>
                
                        <ResponsiveContainer width="100%" height={300}>
                
                            <BarChart
                
                                data={customerAnalytics?.customer_types ?? []}
                
                            >
                
                                <CartesianGrid strokeDasharray="3 3"/>
                
                                <XAxis dataKey="customer_type"/>
                
                                <YAxis/>
                
                                <Tooltip/>
                
                                <Bar
                
                                    dataKey="count"
                
                                    fill="#4caf50"
                
                                />
                
                            </BarChart>
                
                        </ResponsiveContainer>
                
                    </div>
                
                </div>

                <div className="chart-card">

                    <h3>
                        Customer Revenue Analysis
                    </h3>
                
                    {topCustomers.length === 0 ? (
                
                        <div className="analytics-empty">
                
                            No customer revenue data available
                            for the selected period.
                
                        </div>
                
                    ) : (
                
                        <div className="table-wrapper">
                
                            <table className="analytics-table">
                
                                <thead>
                
                                    <tr>
                
                                        <th>Customer Name</th>
                
                                        <th>Orders</th>
                
                                        <th>Total Spend</th>
                
                                        <th>Average Order Value</th>
                
                                    </tr>
                
                                </thead>
                
                                <tbody>
                
                                    {topCustomers.map(
                                        (customer: any, index: number) => (
                
                                        <tr
                                            key={
                                                customer.customer_name ??
                                                index
                                            }
                                        >
                
                                            <td>
                                                {customer.customer_name}
                                            </td>
                
                                            <td>
                                                {customer.total_orders}
                                            </td>
                
                                            <td>
                                                ₹
                                                {Number(
                                                    customer.total_spend ?? 0
                                                ).toLocaleString("en-IN", {
                                                    minimumFractionDigits: 2,
                                                    maximumFractionDigits: 2
                                                })}
                                            </td>
                
                                            <td>
                                                ₹
                                                {Number(
                                                    customer.average_order_value ?? 0
                                                ).toLocaleString("en-IN", {
                                                    minimumFractionDigits: 2,
                                                    maximumFractionDigits: 2
                                                })}
                                            </td>
                
                                        </tr>
                
                                    ))}
                
                                </tbody>
                
                            </table>
                
                        </div>
                
                    )}
                
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

                <div className="analytics-section">

        <div
            style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "15px"
            }}
        >

                <h2>
                    Sales vs Orders
                </h2>
        
                <select
                    value={salesVsOrdersPeriod}
                    onChange={(e) =>
                        setSalesVsOrdersPeriod(e.target.value)
                    }
                    style={{
                        padding: "8px 12px",
                        borderRadius: "6px",
                        border: "1px solid #ccc",
                        background: "#fff",
                        cursor: "pointer"
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
        
        
            <div
                style={{
                    width: "100%",
                    height: "420px",
                    background: "#fff",
                    borderRadius: "12px",
                    padding: "20px",
                    boxSizing: "border-box"
                }}
            >
        
                <ResponsiveContainer
                    width="100%"
                    height="100%"
                >
        
                    <ScatterChart
                        margin={{
                            top: 20,
                            right: 30,
                            bottom: 30,
                            left: 30
                        }}
                    >
        
                        <CartesianGrid
                            strokeDasharray="3 3"
                        />
        
                        {/* ONE X-AXIS */}
                        <XAxis
                            type="number"
                            dataKey="orders"
                            name="Number of Orders"
                            label={{
                                value: "Number of Orders",
                                position: "insideBottom",
                                offset: -15
                            }}
                        />
        
                        {/* ONE Y-AXIS */}
                        <YAxis
                            type="number"
                            dataKey="revenue"
                            name="Revenue"
                            label={{
                                value: "Revenue",
                                angle: -90,
                                position: "insideLeft"
                            }}
                        />
        
                        <Tooltip
                            cursor={{
                                strokeDasharray: "3 3"
                            }}
                            formatter={(value: any, name: any) => {
        
                                if (name === "Revenue") {
        
                                    return [
                                        Number(value).toLocaleString(),
                                        "Revenue"
                                    ];
        
                                }
        
                                return [
                                    value,
                                    "Number of Orders"
                                ];
        
                            }}
                        />
        
                        <Scatter
                            name="Sales vs Orders"
                            data={salesVsOrdersData}
                            fill="#1976d2"
                        />
        
                    </ScatterChart>
        
                </ResponsiveContainer>
        
            </div>
        
        </div>


                <h2 className="section-title">
                    Sales Analytics
                </h2>
                
                <div className="analytics-grid">
                
                    <div className="chart-card">
                
                        <h3>Top 10 Best Selling Products</h3>

                        <select
                            value={productSort}
                            onChange={(e) =>
                                setProductSort(
                                    e.target.value as "quantity" | "revenue"
                                )
                            }
                        >
                            <option value="quantity">Sort by Quantity</option>
                            <option value="revenue">Sort by Revenue</option>
                        </select>
                
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

                        <table className="analytics-table">

                            <thead>
                                <tr>
                                    <th>Product</th>
                                    <th>Quantity Sold</th>
                                    <th>Revenue</th>
                                </tr>
                            </thead>
                        
                            <tbody>
                                {topProducts.length > 0 ? (
                                    topProducts.map((item: any) => (
                                        <tr key={item.product_id ?? item.product_name}>
                                            <td>{item.product_name}</td>
                                            <td>{item.quantity_sold}</td>
                                            <td>₹{Number(item.revenue ?? 0).toLocaleString()}</td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={3}>
                                            No product data available
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        
                        </table>
                
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

                        <table className="analytics-table">

                            <thead>
                                <tr>
                                    <th>Payment Method</th>
                                    <th>Revenue</th>
                                </tr>
                            </thead>
                        
                            <tbody>
                                {paymentMethods.length > 0 ? (
                                    paymentMethods.map((item: any) => (
                                        <tr key={item.payment_method}>
                                            <td>{item.payment_method}</td>
                                            <td>
                                                {Number(item.total_sales ?? 0).toLocaleString()}
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={2}>
                                            No payment method data available
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        
                        </table>
                
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

                <h2 className="section-title">
                    Forecast Charts
                </h2>
                
                <div className="analytics-grid">
                
                    <div className="chart-card">
                
                        <h3>Predicted Demand By Product</h3>
                
                        <ResponsiveContainer width="100%" height={300}>
                
                            <BarChart
                                data={topForecastProducts}
                            >
                
                                <CartesianGrid strokeDasharray="3 3" />
                
                                <XAxis
                                    dataKey="product"
                                    angle={-30}
                                    textAnchor="end"
                                    interval={0}
                                />
                
                                <YAxis />
                
                                <Tooltip />
                
                                <Bar
                                    dataKey="predicted_demand"
                                    fill="#1976d2"
                                />
                
                            </BarChart>
                
                        </ResponsiveContainer>
                
                    </div>
                
                    <div className="chart-card">
                
                        <h3>Demand By Category</h3>
                
                        <ResponsiveContainer width="100%" height={300}>
                
                            <PieChart>
                
                                <Pie
                                    data={categoryTrend}
                                    dataKey="predicted_demand"
                                    nameKey="category"
                                    outerRadius={90}
                                    label
                                />
                
                                <Tooltip />
                
                                <Legend />
                
                            </PieChart>
                
                        </ResponsiveContainer>
                
                    </div>

                    <div className="chart-card">
                    
                    <h3>Historical vs Forecast</h3>
                    
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={historicalForecast}>
                            <CartesianGrid strokeDasharray="3 3" />
                    
                            <XAxis dataKey="product" />
                    
                            <YAxis />
                    
                            <Tooltip />
                    
                            <Legend />
                    
                            <Line
                                type="monotone"
                                dataKey="historical_sales"
                                stroke="#1976d2"
                                strokeWidth={3}
                                name="Historical Sales"
                            />
                    
                            <Line
                                type="monotone"
                                dataKey="forecast"
                                stroke="#ff9800"
                                strokeWidth={3}
                                name="Forecast"
                            />
                        </LineChart>
                    </ResponsiveContainer>
                    
                    </div>
                
                </div>

                <div className="chart-card">

                <h3>Product Demand Trend</h3>
                
                <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={productTrend}>
                        <CartesianGrid strokeDasharray="3 3"/>
                
                        <XAxis dataKey="product"/>
                
                        <YAxis/>
                
                        <Tooltip/>
                
                        <Legend/>
                
                        <Line
                            type="monotone"
                            dataKey="predicted_demand"
                            stroke="#4caf50"
                            strokeWidth={3}
                            name="Predicted Demand"
                        />
                    </LineChart>
                </ResponsiveContainer>
                
                </div>

                <div className="chart-card">

                <h3>Seasonal Sales Pattern</h3>
                
                <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={seasonalPattern}>
                        <CartesianGrid strokeDasharray="3 3"/>
                
                        <XAxis dataKey="month"/>
                
                        <YAxis/>
                
                        <Tooltip/>
                
                        <Legend/>
                
                        <Bar
                            dataKey="sales"
                            fill="#1976d2"
                            name="Sales"
                        />
                    </BarChart>
                </ResponsiveContainer>
                
                </div>

                <h2 className="section-title">
                    Drill Down Analytics
                </h2>
                
                <div className="analytics-grid">
                
                    <div className="chart-card">
                
                        <h3>Categories</h3>
                
                        <table className="analytics-table">
                
                            <thead>
                
                                <tr>
                
                                    <th>Category</th>
                
                                    <th>Total Products</th>
                
                                </tr>
                
                            </thead>
                
                            <tbody>
                
                                {categories.map((cat:any) => (
                
                                    <tr
                                        key={cat.id}
                                        onClick={() => loadProducts(cat.id)}
                                        className={
                                            selectedCategory === cat.id
                                                ? "selected"
                                                : ""
                                        }
                                    >
                
                                        <td>{cat.name}</td>

                                        <td>{cat.total_products}</td>
                
                                    </tr>
                
                                ))}
                
                            </tbody>
                
                        </table>
                
                    </div>


                
                    <div className="chart-card">
                
                        <h3>Products</h3>
                
                        <table className="analytics-table">
                
                            <thead>
                
                                <tr>
                
                                    <th>Product</th>
                
                                    <th>Total Sold</th>
                
                                </tr>
                
                            </thead>
                
                            <tbody>
                
                                {products.map((p:any)=>(
                
                                    <tr
                                        key={p.id}
                                        onClick={() => loadSales(p.id)}
                                        className={
                                            selectedProduct===p.id
                                                ? "selected"
                                                : ""
                                        }
                                    >
                
                                        <td>{p.name}</td>

                                        <td>{p.total_sold}</td>
                
                                    </tr>
                
                                ))}
                
                            </tbody>
                
                        </table>
                
                    </div>
                
                </div>
                
                <div className="chart-card">
                
                    <h3>Sales History</h3>
                
                    <table className="analytics-table">
                
                        <thead>
                        <tr>
                            <th>Invoice</th>
                            <th>Customer</th>
                            <th>Sale Date</th>
                            <th>Quantity</th>
                            <th>Total Amount</th>
                            <th>Payment Method</th>
                            <th>Sales Channel</th>
                        </tr>
                        </thead>
                
                        <tbody>
                
                            {sales.map((sale:any)=>(
                
                                <tr key={sale.invoice_number}>
                
                                    <td>{sale.invoice_number}</td>
                                    <td>{sale.customer_name}</td>
                                    <td>{sale.sale_date}</td>
                                    <td>{sale.quantity}</td>
                                    <td>{sale.total_amount}</td>
                                    <td>{sale.payment_method}</td>
                                    <td>{sale.sales_channel}</td>
                                </tr>
                
                            ))}
                
                        </tbody>
                
                    </table>
                
                </div>

            </div>

        </>

    );

}

export default Analytics;