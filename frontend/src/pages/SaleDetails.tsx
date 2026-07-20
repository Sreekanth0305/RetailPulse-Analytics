import { useEffect, useState } from "react";

import {
  useNavigate,
  useParams,
} from "react-router-dom";

import {
  getSaleById,
} from "../services/saleService";

import "../styles/sales.css";

interface SaleItem {

  product_id: number;

  product_name: string;

  category_id: number;

  category_name: string;

  quantity: number;

  unit_price: number;

  discount: number;

  tax: number;

  total: number;

}

interface SaleDetail {

  id: number;

  invoice_number: string;

  customer_name: string;

  sale_date: string;

  sales_channel: string;

  payment_method: string;

  total_amount: number;

  items: SaleItem[];

}

const SaleDetails = () => {

  const navigate = useNavigate();

  const { saleId } =
    useParams();

  const [sale, setSale] =
    useState<SaleDetail | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

    const loadSale = async () => {

    if (!saleId) {

      setError("Invalid Sale ID");

      setLoading(false);

      return;

    }

    try {

      const data =
        await getSaleById(
          Number(saleId)
        );

      setSale(data);

    } catch (err) {

      console.log(err);

      setError(
        "Unable to load sale."
      );

    } finally {

      setLoading(false);

    }

  };  

    useEffect(() => {

    loadSale();

  }, []);

    if (loading) {

    return (

      <div className="sales-container">

        <h2>
          Loading...
        </h2>

      </div>

    );

  }

    if (error) {

    return (

      <div className="sales-container">

        <h2>

          {error}

        </h2>

      </div>

    );

  }

  return (

<div className="sales-container">

<h2>

Invoice Details

</h2>

<div className="sale-details-card">

<h3>

Invoice Information

</h3>

<p>

<strong>

Invoice Number :

</strong>

{sale?.invoice_number}

</p>

<p>

<strong>

Sale Date :

</strong>

{new Date(
sale!.sale_date
).toLocaleString()}

</p>

</div>

<div className="sale-details-card">

<h3>

Customer Information

</h3>

<p>

<strong>

Customer Name :

</strong>

{sale?.customer_name}

</p>

</div>

<div className="sale-details-card">

<h3>

Sales Information

</h3>

<p>

<strong>

Sales Channel :

</strong>

{sale?.sales_channel}

</p>

<p>

<strong>

Payment Method :

</strong>

{sale?.payment_method}

</p>

</div>

<h3>

Products

</h3>

<table className="sales-table">

<thead>

<tr>

<th>

Product

</th>

<th>

Category

</th>

<th>

Quantity

</th>

<th>

Unit Price

</th>

<th>

Discount

</th>

<th>

Tax

</th>

<th>

Total

</th>

</tr>

</thead>

<tbody>

{sale?.items.map((item)=>(

<tr
key={item.product_id}
>

<td>

{item.product_name}

</td>

<td>

{item.category_name}

</td>

<td>

{item.quantity}

</td>

<td>

₹{item.unit_price}

</td>

<td>

₹{item.discount}

</td>

<td>

₹{item.tax}

</td>

<td>

₹{item.total}

</td>

</tr>

))}

</tbody>

</table>

<div className="sale-summary">

<h3>

Pricing Summary

</h3>

<p>

<strong>

Total Discount :

</strong>

₹{

sale?.items.reduce(

(sum,item)=>

sum+item.discount,

0

)

}

</p>

<p>

<strong>

Total Tax :

</strong>

₹{

sale?.items.reduce(

(sum,item)=>

sum+item.tax,

0

)

}

</p>

<p>

<strong>

Final Amount :

</strong>

₹{

sale?.total_amount

}

</p>

</div>

<button

className="back-btn"

onClick={()=>

navigate("/sales")

}

>

← Back

</button>

</div>

);

};

export default SaleDetails;