import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8001";

const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token");

  return {
    Authorization: `Bearer ${token}`,
  };
};


// Get available report types
export const getReportTypes = async () => {
  const response = await axios.get(
    `${API_BASE_URL}/reports/`,
    {
      headers: getAuthHeaders(),
    }
  );

  return response.data;
};


// Generate report
export const generateReport = async (
  reportType: string,
  filters: Record<string, any> = {},
  page: number = 1,
  limit: number = 10,
  sortBy: string = "id",
  sortOrder: string = "desc"
) => {

  const response = await axios.get(
    `${API_BASE_URL}/reports/${encodeURIComponent(reportType)}`,
    {
      headers: getAuthHeaders(),

      params: {
        filters: JSON.stringify(filters),
        page,
        limit,
        sort_by: sortBy,
        sort_order: sortOrder,
      },
    }
  );

  return response.data;
};


// Export report as CSV
export const exportReportCSV = async (
  reportType: string,
  filters: Record<string, any> = {}
) => {

  const response = await axios.get(
    `${API_BASE_URL}/reports/${encodeURIComponent(reportType)}/export/csv`,
    {
      headers: getAuthHeaders(),

      params: {
        filters: JSON.stringify(filters),
      },

      responseType: "blob",
    }
  );

  return response.data;
};


// Export report as PDF
export const exportReportPDF = async (
  reportType: string,
  filters: Record<string, any> = {}
) => {

  const response = await axios.get(
    `${API_BASE_URL}/reports/${encodeURIComponent(reportType)}/export/pdf`,
    {
      headers: getAuthHeaders(),

      params: {
        filters: JSON.stringify(filters),
      },

      responseType: "blob",
    }
  );

  return response.data;
};