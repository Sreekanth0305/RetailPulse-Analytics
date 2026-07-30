import axios from "../api/axios";

// =========================================
// Dashboard KPI Cards
// =========================================
export const getAnalyticsKPIs = (params?: any) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/analytics/kpis", {

        params,

        headers: {

            Authorization: `Bearer ${token}`,

        },

    });

};

// =========================================
// Revenue Trend
// =========================================
export const getRevenueTrend = (params?: any) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/analytics/revenue-trend", {
        params,
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

// =========================================
// Sales Trend
// =========================================
export const getSalesTrend = (params?: any) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/analytics/sales-trend", {
        params,
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

// =========================================
// Top Selling Products
// =========================================
export const getTopSellingProducts = (params?: any) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/analytics/top-selling-products", {
        params,
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

// =========================================
// Top Categories
// =========================================
export const getTopCategories = (params?: any) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/analytics/top-categories", {
        params,
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

// =========================================
// Sales By Payment Method
// =========================================
export const getPaymentMethodAnalytics = (params?: any) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/analytics/sales-by-payment-method", {
        params,
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

// =========================================
// Sales By Sales Channel
// =========================================
export const getSalesChannelAnalytics = (params?: any) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/analytics/sales-by-sales-channel", {
        params,
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

// =========================================
// Inventory Distribution
// =========================================
export const getInventoryDistribution = (params?: any) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/analytics/inventory-distribution", {
        params,
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

// =========================================
// Stock Status Summary
// =========================================
export const getStockStatusSummary = (params?: any) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/analytics/stock-status-summary", {
        params,
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

// =========================================
// Low Stock Products
// =========================================
export const getLowStockProducts = (params?: any) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/analytics/low-stock-products", {
        params,
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

// =========================================
// Out Of Stock Products
// =========================================
export const getOutOfStockProducts = (params?: any) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/analytics/out-of-stock-products", {
        params,
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

// =========================================
// Inventory Value By Category
// =========================================
export const getInventoryValue = (params?: any) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/analytics/inventory-value-by-category", {
        params,
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

export const getDrilldownCategories = () => {

    const token = localStorage.getItem("access_token");

    return axios.get("/analytics/drilldown/categories", {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

export const getDrilldownProducts = (categoryId: number) => {

    const token = localStorage.getItem("access_token");

    return axios.get(`/analytics/drilldown/products/${categoryId}`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

export const getDrilldownSales = (productId: number) => {

    const token = localStorage.getItem("access_token");

    return axios.get(`/analytics/drilldown/sales/${productId}`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

// =========================================
// Forecast Dashboard KPI
// =========================================

export const getForecastDashboard = () => {

    const token = localStorage.getItem("access_token");

    return axios.get("/analytics/forecast-dashboard", {

        headers: {
            Authorization: `Bearer ${token}`,
        },

    });

};

export const getHistoricalVsForecast = () => {

    const token = localStorage.getItem("access_token");

    return axios.get("/forecast/charts/historical-vs-forecast", {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

export const getProductDemandTrend = () => {

    const token = localStorage.getItem("access_token");

    return axios.get("/forecast/charts/product-trend", {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

export const getCategoryDemandTrend = () => {

    const token = localStorage.getItem("access_token");

    return axios.get("/forecast/charts/category-trend", {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

export const getTopPredictedProducts = () => {

    const token = localStorage.getItem("access_token");

    return axios.get("/forecast/charts/top-products", {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};

export const getSeasonalSalesPattern = () => {

    const token = localStorage.getItem("access_token");

    return axios.get("/forecast/charts/seasonal", {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};