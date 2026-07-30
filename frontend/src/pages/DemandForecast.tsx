import { useEffect, useState } from "react";
import "../styles/demandForecast.css";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import {
  Grid,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button
} from "@mui/material";

import {
  getForecasts,
  getCategoryForecasts,
  getInventoryRecommendations,
  exportForecastCSV,
  exportCategoryCSV,
  exportProductPDF,
} from "../services/forecastService";

const DemandForecast = () => {
  const [forecasts, setForecasts] = useState<any[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [product, setProduct] = useState("");
  const [category, setCategory] = useState("");
  const [brand, setBrand] = useState("");
  const [period, setPeriod] = useState("");
  const [sortBy, setSortBy] = useState("");

  const loadData = async () => {

      try {
    
        const [
          forecastData,
          categoryData,
          recommendationData,
        ] = await Promise.all([
    
          getForecasts({
            product,
            category,
            brand,
            period,
            sort_by: sortBy,
          }),
    
          getCategoryForecasts(),
    
          getInventoryRecommendations(),
    
        ]);
    
        setForecasts(forecastData);
    
        setCategories(categoryData);
    
        setRecommendations(recommendationData);
    
      } catch (error) {
    
        console.error(error);
    
      }
    
    };

  useEffect(() => {

    loadData();
  
  }, [
    product,
    category,
    brand,
    period,
    sortBy
  ]);

  return (
    <>
        <Sidebar />
        <Navbar />
        <div className="forecast-page">
    
          <h2 className="forecast-title">
            Demand Forecasting
          </h2>
          
          <div className="filter-section">
          <h4 className="section-title">
              Forecast Filters
          </h4>
          
          <Grid container spacing={2} sx={{ mb: 4 }}>
          
              <Grid size={{ xs: 12, md: 2 }}>
          
                  <TextField
          
                      fullWidth
          
                      label="Product"
          
                      value={product}
          
                      onChange={(e) => setProduct(e.target.value)}
          
                  />
          
              </Grid>
          
              <Grid size={{ xs: 12, md: 2 }}>
          
                  <TextField
          
                      fullWidth
          
                      label="Category"
          
                      value={category}
          
                      onChange={(e) => setCategory(e.target.value)}
          
                  />
          
              </Grid>
          
              <Grid size={{ xs: 12, md: 2 }}>
          
                  <TextField
          
                      fullWidth
          
                      label="Brand"
          
                      value={brand}
          
                      onChange={(e) => setBrand(e.target.value)}
          
                  />
          
              </Grid>
          
              <Grid size={{ xs: 12, md: 2 }}>
    
                  <FormControl fullWidth>
          
                      <InputLabel>
                          Forecast Period
                      </InputLabel>
          
                      <Select
          
                          value={period}
          
                          label="Forecast Period"
          
                          onChange={(e) => setPeriod(e.target.value)}
          
                      >
          
                          <MenuItem value="">
                              All
                          </MenuItem>
          
                          <MenuItem value="Next 7 days">
                              Next 7 Days
                          </MenuItem>
          
                          <MenuItem value="Next 30 days">
                              Next 30 Days
                          </MenuItem>
          
                          <MenuItem value="Next 90 days">
                              Next 90 Days
                          </MenuItem>
          
                      </Select>
          
                  </FormControl>
          
              </Grid>
          
              <Grid size={{ xs: 12, md: 2 }}>
          
                  <FormControl fullWidth>
          
                      <InputLabel>
                          Sort By
                      </InputLabel>
          
                      <Select
          
                          value={sortBy}
          
                          label="Sort By"
          
                          onChange={(e) => setSortBy(e.target.value)}
          
                      >
          
                          <MenuItem value="">
                              Latest
                          </MenuItem>
          
                          <MenuItem value="highest_demand">
                              Highest Predicted Demand
                          </MenuItem>
          
                          <MenuItem value="lowest_stock">
                              Lowest Stock
                          </MenuItem>
          
                          <MenuItem value="highest_growth">
                              Highest Growth
                          </MenuItem>
          
                          <MenuItem value="accuracy">
                              Forecast Accuracy
                          </MenuItem>
          
                      </Select>
          
                  </FormControl>
          
              </Grid>
          
          </Grid>
          
          </div>
          
          <div className="forecast-card">

          <h3 className="section-title">
              Product Forecasts
          </h3>
          
          <div className="table-responsive">
          
          <table className="table table-bordered table-hover">
          
              <thead>
          
                  <tr>
          
                      <th>Product</th>
          
                      <th>Predicted Demand</th>
          
                      <th>Confidence</th>
          
                      <th>Forecast Period</th>
          
                  </tr>
          
              </thead>
          
              <tbody>
          
                  {forecasts.map((item: any) => (
          
                      <tr key={item.id}>
          
                          <td>{item.product?.name}</td>
          
                          <td>{item.predicted_demand}</td>
          
                          <td>{item.confidence_score}%</td>
          
                          <td>{item.forecast_period}</td>
          
                      </tr>
          
                  ))}
          
              </tbody>
          
          </table>
          
          </div>

          </div>
          
          <div className="forecast-card">

          <h3 className="section-title">
              Category Forecasts
          </h3>
          
          <div className="table-responsive">
          
          <table className="table table-bordered table-hover">
          
              <thead>
          
                  <tr>
          
                      <th>Category</th>
          
                      <th>Predicted Demand</th>
          
                  </tr>
          
              </thead>
          
              <tbody>
          
                  {categories.map((item: any, index: number) => (
          
                      <tr key={index}>
          
                          <td>{item.category}</td>
          
                          <td>{item.predicted_demand}</td>
          
                      </tr>
          
                  ))}
          
              </tbody>
          
          </table>

          </div>

          </div>
    
          <div className="forecast-card">

          <h3 className="section-title">
              Inventory Recommendations
          </h3>
          
          <div className="table-responsive">
          
          <table className="table table-bordered table-hover">
    
            <thead>
    
              <tr>
    
                <th>Product</th>
    
                <th>Current Stock</th>
    
                <th>Predicted Demand</th>
    
                <th>Recommendation</th>
    
              </tr>
    
            </thead>
    
            <tbody>
    
              {recommendations.map((item: any) => (
    
                <tr key={item.product_id}>
    
                  <td>{item.product_name}</td>
    
                  <td>{item.current_stock}</td>
    
                  <td>{item.predicted_demand}</td>
    
                  <td>{item.recommendation}</td>
    
                </tr>
    
              ))}
    
            </tbody>
    
          </table>

          </div>

          </div>
    
          <div className="forecast-actions">
    
              <Button
                  variant="contained"
                  color="primary"
                  onClick={exportForecastCSV}
              >
                  Export Forecast CSV
              </Button>
          
              <Button
                  variant="contained"
                  color="success"
                  onClick={exportCategoryCSV}
              >
                  Export Category CSV
              </Button>
          
              <Button
                  variant="contained"
                  color="secondary"
                  onClick={exportProductPDF}
              >
                  Export Product PDF
              </Button>
          
          </div>
    
        </div>
    </>
  );
};

export default DemandForecast;