import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import {
  getSales,
  searchSales,
  filterSales,
  sortSales,
  deleteSale,
} from "../services/saleService";

import SaleForm from "../components/SaleForm";

import "../styles/sales.css";

interface Sale {
  id: number;
  invoice_number: string;
  customer_name: string;
  product_name:string;
  sale_date: string;
  sales_channel: string;
  payment_method: string;
  total_amount: number;
}

const Sales = () => {
  const navigate = useNavigate();
  const [sales, setSales] = useState<Sale[]>([]);
  const [keyword, setKeyword] = useState("");

  const [sortBy, setSortBy] = useState("");

  const [filters, setFilters] = useState({
    start_date: "",
    end_date: "",
    category_id: undefined as number | undefined,
    sales_channel: "",
    payment_method: "",
  });

  const [showForm, setShowForm] = useState(false);

  const [editingSaleId, setEditingSaleId] =
    useState<number | undefined>(undefined);

  useEffect(() => {
    loadSales();
  }, []);

  const loadSales = async () => {
    try {
      const data = await getSales();
      setSales(data);
    } catch (err) {
      console.log(err);
    }
  };

  const handleSearch = async () => {
    if (!keyword) {
      loadSales();
      return;
    }

    try {
      const data = await searchSales(keyword);
      setSales(data);
    } catch (err) {
      console.log(err);
    }
  };

  const handleFilter = async () => {
    try {
      const data = await filterSales(filters);
      setSales(data);
    } catch (err) {
      console.log(err);
    }
  };

  const handleSort = async (value: string) => {
    setSortBy(value);

    if (!value) {
      loadSales();
      return;
    }

    try {
      const data = await sortSales(value);
      setSales(data);
    } catch (err) {
      console.log(err);
    }
  };

  const handleDelete = async (id: number) => {
    const confirmDelete = window.confirm(
      "Delete this sale?"
    );

    if (!confirmDelete) return;

    try {
      await deleteSale(id);
      loadSales();
    } catch (err) {
      console.log(err);
    }
  };

  return (
   <>
    <Sidebar />
    <Navbar />

    <div className="sales-container">

      <div className="sales-header">
        <h2>Sales Management</h2>

        <button
          onClick={() => {
            setEditingSaleId(undefined);
            setShowForm(true);
          }}
        >
          + Add Sale
        </button>
      </div>

      {/* Search */}

      <div className="sales-search">

        <input
          type="text"
          placeholder="Search Invoice / Customer / Product"
          value={keyword}
          onChange={(e) =>
            setKeyword(e.target.value)
          }
        />

        <button onClick={handleSearch}>
          Search
        </button>

      </div>

      {/* Filters */}

      <div className="sales-filters">

        <input
          type="date"
          value={filters.start_date}
          onChange={(e) =>
            setFilters({
              ...filters,
              start_date: e.target.value,
            })
          }
        />

        <input
          type="date"
          value={filters.end_date}
          onChange={(e) =>
            setFilters({
              ...filters,
              end_date: e.target.value,
            })
          }
        />

        <select
          value={filters.sales_channel}
          onChange={(e) =>
            setFilters({
              ...filters,
              sales_channel: e.target.value,
            })
          }
        >
          <option value="">Sales Channel</option>

          <option value="Retail Store">
            Retail Store
          </option>

          <option value="Online Store">
            Online Store
          </option>

          <option value="Marketplace">
            Marketplace
          </option>
        </select>

        <select
          value={filters.payment_method}
          onChange={(e) =>
            setFilters({
              ...filters,
              payment_method: e.target.value,
            })
          }
        >
          <option value="">Payment</option>

          <option value="Cash">Cash</option>

          <option value="Card">Card</option>

          <option value="UPI">UPI</option>

          <option value="Bank Transfer">
            Bank Transfer
          </option>
        </select>

        <button onClick={handleFilter}>
          Apply Filter
        </button>

      </div>

      {/* Sorting */}

      <div className="sales-sort">

        <label>Sort By :</label>

        <select
          value={sortBy}
          onChange={(e) =>
            handleSort(e.target.value)
          }
        >
          <option value="">
            Select
          </option>

          <option value="date">
            Date
          </option>

          <option value="invoice">
            Invoice
          </option>

          <option value="amount">
            Amount
          </option>

        </select>

      </div>

        {showForm && (
          <div className="sale-form-container">
        
            <SaleForm
              saleId={editingSaleId}
              onSuccess={() => {
                setShowForm(false);
                loadSales();
              }}
            />
        
            <button
              onClick={() => {
                setShowForm(false);
              }}
            >
              Cancel
            </button>
        
          </div>
        )}

      {/* Table */}

      <table className="sales-table">

        <thead>

          <tr>

            <th>Invoice</th>

            <th>Customer</th>

            <th>Product</th>

            <th>Date</th>

            <th>Channel</th>

            <th>Payment</th>

            <th>Total</th>

            <th>Actions</th>

          </tr>

        </thead>

        <tbody>

          {sales.map((sale) => (

            <tr key={sale.id}>

              <td>{sale.invoice_number}</td>

              <td>{sale.customer_name}</td>

              <td>{sale.product_name}</td>

              <td>
                {new Date(
                  sale.sale_date
                ).toLocaleString()}
              </td>

              <td>{sale.sales_channel}</td>

              <td>{sale.payment_method}</td>

              <td>₹{sale.total_amount}</td>

              <td>

                <button
                  onClick={() =>
                    navigate(`/sales/${sale.id}`)
                  }
                >
                  View
                </button>

                <button
                  onClick={() => {
                    setEditingSaleId(sale.id);
                    setShowForm(true);
                  }}
                >
                  Edit
                </button>

                <button
                  onClick={() =>
                    handleDelete(sale.id)
                  }
                >
                  Delete
                </button>

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  </>
  );
};

export default Sales;