import axios from "axios";

const API = "http://127.0.0.1:8001/forecast";

const authHeader = () => ({
  headers: {
    Authorization: `Bearer ${localStorage.getItem("access_token")}`,
  },
});

export const getForecasts = async (filters?: {
  product?: string;
  category?: string;
  brand?: string;
  period?: string;
  sort_by?: string;
}) => {

  const response = await axios.get(API + "/", {

    ...authHeader(),

    params: filters,

  });

  return response.data;

};

export const getProductForecasts = async () => {
  const response = await axios.get(
    API + "/product",
    authHeader()
  );

  return response.data;
};

export const getCategoryForecasts = async () => {
  const response = await axios.get(
    API + "/category",
    authHeader()
  );

  return response.data;
};

export const getInventoryRecommendations = async () => {
  const response = await axios.get(
    API + "/recommendations",
    authHeader()
  );

  return response.data;
};

export const generateForecast = async (
  forecast_period: string
) => {
  const response = await axios.post(
    API + `/generate?forecast_period=${forecast_period}`,
    {},
    authHeader()
  );

  return response.data;
};

export const generateForecastNotifications = async () => {
  const response = await axios.post(
    API + "/notifications",
    {},
    authHeader()
  );

  return response.data;
};

export const exportForecastCSV = () => {
  window.open(
    API + "/export/csv",
    "_blank"
  );
};

export const exportCategoryCSV = () => {
  window.open(
    API + "/export/category/csv",
    "_blank"
  );
};

export const exportProductPDF = () => {
  window.open(
    API + "/export/product/pdf",
    "_blank"
  );
};