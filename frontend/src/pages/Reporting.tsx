import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import {
  getReportTypes,
  generateReport,
  exportReportCSV,
  exportReportPDF,
} from "../services/reportService";

import ScheduledReports from "../components/ScheduledReports";

import { getProducts } from "../services/productService";
import { getCategories } from "../services/categoryService";
import { getCustomers } from "../services/customerService";
import { getUsers } from "../services/userService";

import "../styles/reporting.css";

interface ReportData {
  report_type: string;
  generated_at: string;
  filters: Record<string, any>;
  items: Record<string, any>[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

interface Product {
  id: number;
  name: string;
}

interface Category {
  id: number;
  name: string;
}

interface Customer {
  id: number;
  full_name: string;
}

interface User {
  id: number;
  name: string;
}

const Reporting = () => {
  const [reportTypes, setReportTypes] = useState<string[]>([]);

  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [users, setUsers] = useState<User[]>([]);

  const [selectedReport, setSelectedReport] = useState("");

  const [report, setReport] = useState<ReportData | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [page, setPage] = useState(1);

  const limit = 10;

  // Report filters
  const [filters, setFilters] = useState({
    start_date: "",
    end_date: "",
    product_id: "",
    category_id: "",
    brand: "",
    customer: "",
    sales_status: "",
    stock_status: "",
    user_id: "",
  });

  // Load reporting data
  // Load reporting data
  // Load reporting data
useEffect(() => {
  const loadReportingData = async () => {
    try {
      const [
        reportTypeData,
        productResponse,
        categoryResponse,
        customerResponse,
        userResponse,
      ] = await Promise.all([
        getReportTypes(),
        getProducts(),
        getCategories(),
        getCustomers(),
        getUsers(),
      ]);

      setReportTypes(reportTypeData.report_types);

      setProducts(productResponse.data);
      setCategories(categoryResponse.data);
      setCustomers(customerResponse.data);
      setUsers(userResponse.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load reporting data.");
    }
  };

  loadReportingData();
}, []);

  // Get currently applied filters
  const getAppliedFilters = () => {
    const applied: string[] = [];

    if (filters.start_date) {
      applied.push(`Start Date: ${filters.start_date}`);
    }

    if (filters.end_date) {
      applied.push(`End Date: ${filters.end_date}`);
    }

    if (filters.product_id) {
      const product = products.find(
        (item) => String(item.id) === filters.product_id
      );

      applied.push(
        `Product: ${product?.name ?? filters.product_id}`
      );
    }

    if (filters.category_id) {
      const category = categories.find(
        (item) => String(item.id) === filters.category_id
      );

      applied.push(
        `Category: ${category?.name ?? filters.category_id}`
      );
    }

    if (filters.brand) {
      applied.push(`Brand: ${filters.brand}`);
    }

    if (filters.customer) {
      applied.push(`Customer: ${filters.customer}`);
    }

    if (filters.sales_status) {
      applied.push(
        `Sales Status: ${filters.sales_status}`
      );
    }

    if (filters.stock_status) {
      applied.push(
        `Stock Status: ${filters.stock_status}`
      );
    }

    if (filters.user_id) {
      const user = users.find(
        (item) => String(item.id) === filters.user_id
      );

      applied.push(
        `User: ${user?.name ?? filters.user_id}`
      );
    }

    return applied;
  };

  // Generate report
  const handleGenerateReport = async () => {
    if (!selectedReport) {
      setError("Please select a report type.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      console.log("SELECTED REPORT:", selectedReport);
      console.log("FILTERS BEING SENT:", filters);

      const data = await generateReport(
        selectedReport,
        filters,
        page,
        limit,
        "id",
        "desc"
      );

      setReport(data);
    } catch (err) {
      console.error(err);
      setReport(null);
      setError("Failed to generate report.");
    } finally {
      setLoading(false);
    }
  };

  const handleExportCSV = async () => {
    if (!selectedReport) {
      setError("Please select a report type.");
      return;
    }
  
    try {
      setError("");
  
      const blob = await exportReportCSV(
        selectedReport,
        filters
      );
  
      const url = window.URL.createObjectURL(blob);
  
      const link = document.createElement("a");
      link.href = url;
      link.download = `${selectedReport.replace(
        /\s+/g,
        "_"
      )}.csv`;
  
      document.body.appendChild(link);
      link.click();
  
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      setError("Failed to export CSV report.");
    }
  };
  
  const handleExportPDF = async () => {
    if (!selectedReport) {
      setError("Please select a report type.");
      return;
    }
  
    try {
      setError("");
  
      const blob = await exportReportPDF(
        selectedReport,
        filters
      );
  
      const url = window.URL.createObjectURL(blob);
  
      const link = document.createElement("a");
      link.href = url;
      link.download = `${selectedReport.replace(
        /\s+/g,
        "_"
      )}.pdf`;
  
      document.body.appendChild(link);
      link.click();
  
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      setError("Failed to export PDF report.");
    }
  };

  // Change page
  const handlePageChange = async (newPage: number) => {
    if (
      newPage < 1 ||
      (report && newPage > report.total_pages)
    ) {
      return;
    }

    setPage(newPage);

    if (!selectedReport) {
      return;
    }

    try {
      setLoading(true);
      setError("");

      const data = await generateReport(
        selectedReport,
        filters,
        newPage,
        limit,
        "id",
        "desc"
      );

      setReport(data);
    } catch (err) {
      console.error(err);
      setError("Failed to load report page.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Sidebar />

      <Navbar />

      <div className="reporting-page">
        <div className="reporting-header">
          <div>
            <h1>Reporting</h1>

            <p>
              Generate and view business reports
              from your RetailPulse data.
            </p>
          </div>
        </div>

        {/* Report selection and filters */}

        <div className="report-controls">
          <div className="report-field">
            <label htmlFor="reportType">
              Report Type
            </label>

            <select
              id="reportType"
              value={selectedReport}
              onChange={(e) => {
                setSelectedReport(e.target.value);
                setReport(null);
                setPage(1);
                setError("");
              }}
            >
              <option value="">
                Select Report Type
              </option>

              {reportTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          <div className="report-field">
            <label htmlFor="startDate">
              Start Date
            </label>

            <input
              id="startDate"
              type="date"
              value={filters.start_date}
              onChange={(e) =>
                setFilters({
                  ...filters,
                  start_date: e.target.value,
                })
              }
            />
          </div>

          <div className="report-field">
            <label htmlFor="endDate">
              End Date
            </label>

            <input
              id="endDate"
              type="date"
              value={filters.end_date}
              onChange={(e) =>
                setFilters({
                  ...filters,
                  end_date: e.target.value,
                })
              }
            />
          </div>

          <div className="report-field">
            <label htmlFor="product">
              Product
            </label>

            <select
              id="product"
              value={filters.product_id}
              onChange={(e) =>
                setFilters({
                  ...filters,
                  product_id: e.target.value,
                })
              }
            >
              <option value="">
                All Products
              </option>

              {products.map((product) => (
                <option
                  key={product.id}
                  value={product.id}
                >
                  {product.name}
                </option>
              ))}
            </select>
          </div>

          <div className="report-field">
            <label htmlFor="category">
              Category
            </label>

            <select
              id="category"
              value={filters.category_id}
              onChange={(e) =>
                setFilters({
                  ...filters,
                  category_id: e.target.value,
                })
              }
            >
              <option value="">
                All Categories
              </option>

              {categories.map((category) => (
                <option
                  key={category.id}
                  value={category.id}
                >
                  {category.name}
                </option>
              ))}
            </select>
          </div>

          <div className="report-field">
            <label htmlFor="brand">
              Brand
            </label>

            <input
              id="brand"
              type="text"
              placeholder="Enter brand"
              value={filters.brand}
              onChange={(e) =>
                setFilters({
                  ...filters,
                  brand: e.target.value,
                })
              }
            />
          </div>

          <div className="report-field">
            <label htmlFor="customer">
              Customer
            </label>

            <select
              id="customer"
              value={filters.customer}
              onChange={(e) =>
                setFilters({
                  ...filters,
                  customer: e.target.value,
                })
              }
            >
              <option value="">
                All Customers
              </option>

              {customers.map((customer) => (
                <option
                  key={customer.id}
                  value={customer.full_name}
                >
                  {customer.full_name}
                </option>
              ))}
            </select>
          </div>

          <div className="report-field">
            <label htmlFor="salesStatus">
              Sales Status
            </label>

            <select
              id="salesStatus"
              value={filters.sales_status}
              onChange={(e) =>
                setFilters({
                  ...filters,
                  sales_status: e.target.value,
                })
              }
            >
              <option value="">
                All Sales Status
              </option>

              <option value="Paid">
                Paid
              </option>

              <option value="Pending">
                Pending
              </option>

              <option value="Failed">
                Failed
              </option>
            </select>
          </div>

          <div className="report-field">
            <label htmlFor="stockStatus">
              Stock Status
            </label>

            <select
              id="stockStatus"
              value={filters.stock_status}
              onChange={(e) =>
                setFilters({
                  ...filters,
                  stock_status: e.target.value,
                })
              }
            >
              <option value="">
                All Stock Status
              </option>

              <option value="In Stock">
                In Stock
              </option>

              <option value="Low Stock">
                Low Stock
              </option>

              <option value="Out of Stock">
                Out of Stock
              </option>
            </select>
          </div>

          <div className="report-field">
            <label htmlFor="user">
              User
            </label>

            <select
              id="user"
              value={filters.user_id}
              onChange={(e) =>
                setFilters({
                  ...filters,
                  user_id: e.target.value,
                })
              }
            >
              <option value="">
                All Users
              </option>

              {users.map((user) => (
                <option
                  key={user.id}
                  value={user.id}
                >
                  {user.name}
                </option>
              ))}
            </select>
          </div>

          <button
            className="generate-report-btn"
            onClick={handleGenerateReport}
            disabled={loading}
          >
            {loading
              ? "Generating..."
              : "Generate Report"}
          </button>

          <button
            className="clear-filters-btn"
            onClick={() => {
              setFilters({
                start_date: "",
                end_date: "",
                product_id: "",
                category_id: "",
                brand: "",
                customer: "",
                sales_status: "",
                stock_status: "",
                user_id: "",
              });

              setReport(null);
              setPage(1);
              setError("");
            }}
            disabled={loading}
          >
            Clear Filters
          </button>
        </div>

        {/* Error */}

        {error && (
          <div className="report-error">
            {error}
          </div>
        )}

        {/* Loading */}

        {loading && (
          <div className="report-loading">
            Generating report...
          </div>
        )}

        {/* Report */}

        {!loading && report && (
          <div className="report-result">
            <div className="report-summary">
              <div>
                <h2>{report.report_type}</h2>
            
                <p>
                  Generated at:{" "}
                  {new Date(report.generated_at).toLocaleString()}
                </p>
              </div>
            
              <div className="report-summary-actions">
                <div className="report-total">
                  <span>Total Records</span>
                  <strong>{report.total}</strong>
                </div>
            
                <button
                  className="export-csv-btn"
                  onClick={handleExportCSV}
                >
                  Export CSV
                </button>
            
                <button
                  className="export-pdf-btn"
                  onClick={handleExportPDF}
                >
                  Export PDF
                </button>
              </div>
            </div>

            {/* Applied Filters */}

            <div className="applied-filters">
              <strong>
                Applied Filters:
              </strong>

              {getAppliedFilters().length === 0 ? (
                <span>
                  No filters applied
                </span>
              ) : (
                <div className="applied-filter-list">
                  {getAppliedFilters().map(
                    (filter, index) => (
                      <span
                        className="filter-tag"
                        key={index}
                      >
                        {filter}
                      </span>
                    )
                  )}
                </div>
              )}
            </div>

            {/* Empty */}

            {report.items.length === 0 ? (
              <div className="report-empty">
                No data found for this report.
              </div>
            ) : (
              <div className="report-table-container">
                <table className="report-table">
                  <thead>
                    <tr>
                      {Object.keys(
                        report.items[0]
                      ).map((key) => (
                        <th key={key}>
                          {key.replace(
                            /_/g,
                            " "
                          )}
                        </th>
                      ))}
                    </tr>
                  </thead>

                  <tbody>
                    {report.items.map(
                      (item, index) => (
                        <tr key={index}>
                          {Object.keys(item).map(
                            (key) => (
                              <td key={key}>
                                {String(
                                  item[key] ?? "-"
                                )}
                              </td>
                            )
                          )}
                        </tr>
                      )
                    )}
                  </tbody>
                </table>
              </div>
            )}

            {/* Pagination */}

            {report.total_pages > 1 && (
              <div className="report-pagination">
                <button
                  onClick={() =>
                    handlePageChange(page - 1)
                  }
                  disabled={page === 1}
                >
                  Previous
                </button>

                <span>
                  Page {report.page} of{" "}
                  {report.total_pages}
                </span>

                <button
                  onClick={() =>
                    handlePageChange(page + 1)
                  }
                  disabled={
                    page === report.total_pages
                  }
                >
                  Next
                </button>
              </div>
            )}
          </div>
        )}

        {/* Scheduled Reports */}
      <ScheduledReports
        reportTypes={reportTypes}
        filters={filters}
        getAppliedFilters={getAppliedFilters}
      />
      
      </div>
    </>
  );
};

export default Reporting;