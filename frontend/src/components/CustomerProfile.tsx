import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";

interface CustomerSummary {
  total_orders: number;
  total_revenue: number;
  average_order_value: number;
  purchase_frequency: number;
  favorite_product: number;
  favorite_category: number;
  first_purchase: string;
  last_purchase: string;
}

interface CustomerProfile {
  id: number;
  customer_id: string;
  full_name: string;
  email: string;
  phone: string;
  customer_type: string;
  preferred_sales_channel: string;
  status: string;
  city: string;
  state: string;
  country: string;
  summary: CustomerSummary;
}

const CustomerProfile = () => {

  const [customer, setCustomer] = useState<CustomerProfile | null>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [timeline, setTimeline] = useState<any[]>([]);

  const navigate = useNavigate();
  const { customerId } = useParams();

  useEffect(() => {

    const token = localStorage.getItem("access_token");

    axios
        .get(
            `http://127.0.0.1:8001/customer-profile/${customerId}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )

        .then((response) => {

            setCustomer(response.data);

            return axios.get(
                `http://127.0.0.1:8001/sales/customer/${response.data.full_name}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

        })

        .then((res) => {

            setHistory(res.data);

            return axios.get(
                `http://127.0.0.1:8001/customer-timeline/${customerId}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

        })

        .then((timelineResponse) => {

            setTimeline(timelineResponse.data);

            setLoading(false);

        })

        .catch((error) => {

            console.error(error);

            setLoading(false);

        });

}, [customerId]);

  if (loading) {
    return <h2>Loading...</h2>;
  }

  if (!customer) {
    return <h2>No Customer Found</h2>;
  }

  return (
    <div style={{ padding: "20px" }}>

      <h2>Customer Profile</h2>

      <hr />

      <h3>Basic Details</h3>

      <p><strong>Name:</strong> {customer.full_name}</p>
      <p><strong>Email:</strong> {customer.email}</p>
      <p><strong>Phone:</strong> {customer.phone}</p>
      <p><strong>Customer Type:</strong> {customer.customer_type}</p>
      <p><strong>Status:</strong> {customer.status}</p>
      <p><strong>City:</strong> {customer.city}</p>
      <p><strong>State:</strong> {customer.state}</p>
      <p><strong>Country:</strong> {customer.country}</p>

      <hr />

      <h3>Purchase Summary</h3>

      <p><strong>Total Orders:</strong> {customer.summary.total_orders}</p>

      <p><strong>Total Revenue:</strong> ₹{customer.summary.total_revenue}</p>

      <p>
        <strong>Average Order Value:</strong> ₹
        {customer.summary.average_order_value}
      </p>

      <p>
        <strong>Purchase Frequency:</strong>{" "}
        {customer.summary.purchase_frequency}
      </p>

      <p>
        <strong>Favorite Product ID:</strong>{" "}
        {customer.summary.favorite_product}
      </p>

      <p>
        <strong>Favorite Category ID:</strong>{" "}
        {customer.summary.favorite_category}
      </p>

      <p>
        <strong>First Purchase:</strong>{" "}
        {customer.summary.first_purchase}
      </p>

      <p>
        <strong>Last Purchase:</strong>{" "}
        {customer.summary.last_purchase}
      </p>

      <hr />

      <h3>Purchase History</h3>

      <table border={1} cellPadding={8} style={{ borderCollapse: "collapse", width: "100%" }}>
        <thead>
          <tr>
            <th>Invoice</th>
            <th>Date</th>
            <th>Sales Channel</th>
            <th>Payment</th>
            <th>Total</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>

          {history.length > 0 ? (

            history.map((sale) => (

              <tr key={sale.id}>

                <td>{sale.invoice_number}</td>

                <td>{sale.sale_date}</td>

                <td>{sale.sales_channel}</td>

                <td>{sale.payment_method}</td>

                <td>₹{sale.total_amount}</td>

                <td>

                  <button
                    onClick={() =>
                      navigate(`/sales/${sale.id}`)
                    }
                  >
                    View Sale
                  </button>

                </td>

              </tr>

            ))

          ) : (

            <tr>
              <td colSpan={6} style={{ textAlign: "center" }}>
                No Purchase History
              </td>
            </tr>

          )}

        </tbody>

      </table>

      <hr />

        <h3>Customer Timeline</h3>
        
        <table
            border={1}
            cellPadding={8}
            style={{
                borderCollapse: "collapse",
                width: "100%"
            }}
        >
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Activity</th>
                    <th>Description</th>
                </tr>
            </thead>
        
            <tbody>
        
                {timeline.length > 0 ? (
        
                    timeline.map((item: any) => (
        
                        <tr key={item.id}>
        
                            <td>{item.created_at}</td>
        
                            <td>{item.activity}</td>
        
                            <td>{item.description}</td>
        
                        </tr>
        
                    ))
        
                ) : (
        
                    <tr>
        
                        <td
                            colSpan={3}
                            style={{ textAlign: "center" }}
                        >
                            No Timeline Available
                        </td>
        
                    </tr>
        
                )}
        
            </tbody>
        
        </table>
        
    </div>
  );
};

export default CustomerProfile;