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

// =========================================
// Drill Down Analytics
// =========================================
export const getDrillDownAnalytics = (params?: any) => {

    const token = localStorage.getItem("access_token");

    return axios.get("/analytics/drill-down", {
        params,
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

};