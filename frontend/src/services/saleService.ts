import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8001",
});

// Automatically send JWT token
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// -------------------------
// Get All Sales
// -------------------------
export const getSales = async () => {
  const response = await API.get("/sales/");
  return response.data;
};

// -------------------------
// Get Sale Details
// -------------------------
export const getSaleById = async (id: number) => {
  const response = await API.get(`/sales/${id}`);
  return response.data;
};

// -------------------------
// Create Sale
// -------------------------
export const createSale = async (sale: any) => {
  const response = await API.post("/sales/", sale);
  return response.data;
};

// -------------------------
// Update Sale
// -------------------------
export const updateSale = async (
  id: number,
  sale: any
) => {
  const response = await API.put(`/sales/${id}`, sale);
  return response.data;
};

// -------------------------
// Delete Sale
// -------------------------
export const deleteSale = async (id: number) => {
  const response = await API.delete(`/sales/${id}`);
  return response.data;
};

// -------------------------
// Search
// -------------------------
export const searchSales = async (keyword: string) => {
  const response = await API.get("/sales/search", {
    params: {
      keyword,
    },
  });

  return response.data;
};

// -------------------------
// Filter
// -------------------------
export const filterSales = async (filters: {
  start_date?: string;
  end_date?: string;
  category_id?: number;
  sales_channel?: string;
  payment_method?: string;
}) => {
  const response = await API.get("/sales/filter", {
    params: filters,
  });

  return response.data;
};

// -------------------------
// Sort
// -------------------------
export const sortSales = async (sort_by: string) => {
  const response = await API.get("/sales/sort", {
    params: {
      sort_by,
    },
  });

  return response.data;
};