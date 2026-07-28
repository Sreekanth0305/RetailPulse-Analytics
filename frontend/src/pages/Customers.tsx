import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import CustomerForm from "../components/CustomerForm";

import {
    getCustomers,
    deleteCustomer,
    changeCustomerStatus,
    createCustomer,
    updateCustomer
} from "../services/customerService";

import "../styles/customers.css";

function Customers() {

    const navigate = useNavigate();

    const [customers, setCustomers] = useState<any[]>([]);

    const [search, setSearch] = useState("");

    const [customerType, setCustomerType] = useState("");

    const [statusFilter, setStatusFilter] = useState("");
    
    const [cityFilter, setCityFilter] = useState("");
    
    const [stateFilter, setStateFilter] = useState("");
    
    const [countryFilter, setCountryFilter] = useState("");
    
    const [registrationDate, setRegistrationDate] = useState("");
    
    const [sortBy, setSortBy] = useState("name");

    const [openForm,setOpenForm]=useState(false);

    const [selectedCustomer,setSelectedCustomer]=useState<any>(null);

    const loadCustomers = async () => {

        try {
    
            const response = await getCustomers({
    
                search,
    
                customer_type: customerType,
    
                status: statusFilter,
    
                city: cityFilter,
    
                state: stateFilter,
    
                country: countryFilter,
    
                registration_date: registrationDate,
    
                sort_by: sortBy
    
            });
    
            setCustomers(response.data);
    
        }
    
        catch (error) {
    
            console.log(error);
    
        }
    
    };

    useEffect(() => {

        loadCustomers();
    
    }, [
    
        search,
    
        customerType,
    
        statusFilter,
    
        cityFilter,
    
        stateFilter,
    
        countryFilter,
    
        registrationDate,
    
        sortBy
    
    ]);

    const handleDelete = async (id: number) => {

        if (!window.confirm("Delete this customer?")) {

            return;

        }

        try {

            await deleteCustomer(id);

            loadCustomers();

        }

        catch (error) {

            console.log(error);

        }

    };

    const handleStatus = async (

        id: number,

        status: string

    ) => {

        try {

            await changeCustomerStatus(id, status);

            loadCustomers();

        }

        catch (error) {

            console.log(error);

        }

    };

    const handleSaveCustomer = async(customer:any)=>{

        try{
    
            if(selectedCustomer){
    
                await updateCustomer(
                    selectedCustomer.id,
                    customer
                );
    
            }
    
            else{
    
                await createCustomer(customer);
    
            }
    
            setOpenForm(false);
    
            loadCustomers();
    
        }
    
        catch(err){
    
            console.log(err);
    
        }

    };

    return (

        <>

            <Sidebar />

            <Navbar />

            <div className="customers-page">

                <div className="customers-header">

                    <h1>

                        Customers

                    </h1>

                    <button
                        onClick={()=>{
                            setSelectedCustomer(null);
                            setOpenForm(true);
                        }}
                    >
                        Add Customer
                    </button>

                </div>

                <div className="search-box">

                    {/* Search */}
                    <input
                        type="text"
                        placeholder="Search Name / ID / Email / Phone"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                
                    {/* Customer Type */}
                    <select
                        value={customerType}
                        onChange={(e) => setCustomerType(e.target.value)}
                    >
                        <option value="">All Types</option>
                        <option value="Retail">Retail</option>
                        <option value="Wholesale">Wholesale</option>
                        <option value="Corporate">Corporate</option>
                    </select>
                
                    {/* Status */}
                    <select
                        value={statusFilter}
                        onChange={(e) => setStatusFilter(e.target.value)}
                    >
                        <option value="">All Status</option>
                        <option value="Active">Active</option>
                        <option value="Inactive">Inactive</option>
                    </select>
                
                    {/* City */}
                    <input
                        type="text"
                        placeholder="City"
                        value={cityFilter}
                        onChange={(e) => setCityFilter(e.target.value)}
                    />
                
                    {/* State */}
                    <input
                        type="text"
                        placeholder="State"
                        value={stateFilter}
                        onChange={(e) => setStateFilter(e.target.value)}
                    />
                
                    {/* Country */}
                    <input
                        type="text"
                        placeholder="Country"
                        value={countryFilter}
                        onChange={(e) => setCountryFilter(e.target.value)}
                    />
                
                    {/* Registration Date */}
                    <input
                        type="date"
                        value={registrationDate}
                        onChange={(e) => setRegistrationDate(e.target.value)}
                    />
                
                    {/* Sort */}
                    <select
                        value={sortBy}
                        onChange={(e) => setSortBy(e.target.value)}
                    >
                        <option value="name">Sort By Name</option>
                        <option value="total_spend">Total Spend</option>
                        <option value="total_orders">Total Orders</option>
                        <option value="last_purchase">Last Purchase</option>
                        <option value="customer_since">Customer Since</option>
                    </select>
                
                </div>

                <table className="customers-table">

                    <thead>

                        <tr>

                            <th>Customer ID</th>

                            <th>Name</th>

                            <th>Email</th>

                            <th>Phone</th>

                            <th>City</th>

                            <th>Type</th>

                            <th>Segment</th>

                            <th>Status</th>

                            <th>Actions</th>

                        </tr>

                    </thead>

                    <tbody>

                        {

                            customers.map((customer) => (

                                <tr key={customer.id}>

                                    <td>

                                        {customer.customer_id}

                                    </td>

                                    <td>

                                        {customer.full_name}

                                    </td>

                                    <td>

                                        {customer.email}

                                    </td>

                                    <td>

                                        {customer.phone}

                                    </td>

                                    <td>

                                        {customer.city}

                                    </td>

                                    <td>

                                        {customer.customer_type}

                                    </td>

                                    <td>

                                        {customer.segment}

                                    </td>

                                    <td>

                                        {customer.status}

                                    </td>

                                    <td>

                                        <button
                                            onClick={() =>
                                                navigate(`/customer-profile/${customer.id}`)
                                            }
                                        >
                                            View
                                        </button>

                                        <button

                                            onClick={() => {
                                        
                                                setSelectedCustomer(customer);
                                        
                                                setOpenForm(true);
                                        
                                            }}
                                        
                                        >
                                        
                                            Edit
                                        
                                        </button>

                                        <button

                                            onClick={() =>

                                                handleDelete(customer.id)

                                            }

                                        >

                                            Delete

                                        </button>

                                        {

                                            customer.status === "Active"

                                            ?

                                            <button

                                                onClick={() =>

                                                    handleStatus(

                                                        customer.id,

                                                        "Inactive"

                                                    )

                                                }

                                            >

                                                Deactivate

                                            </button>

                                            :

                                            <button

                                                onClick={() =>

                                                    handleStatus(

                                                        customer.id,

                                                        "Active"

                                                    )

                                                }

                                            >

                                                Activate

                                            </button>

                                        }

                                    </td>

                                </tr>

                            ))

                        }

                    </tbody>

                </table>

                <CustomerForm

                    open={openForm}
                
                    onClose={() => setOpenForm(false)}
                
                    initialData={selectedCustomer}
                
                    onSubmit={handleSaveCustomer}
                
                />

            </div>

        </>

    );

}

export default Customers;