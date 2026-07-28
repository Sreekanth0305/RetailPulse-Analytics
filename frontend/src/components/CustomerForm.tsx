import { useEffect, useState } from "react";

interface CustomerFormProps {

    open: boolean;

    onClose: () => void;

    onSubmit: (customer:any)=>Promise<void>;

    initialData?: any;

}

function CustomerForm({

    open,

    onClose,

    onSubmit,

    initialData

}:CustomerFormProps){

    const [form,setForm]=useState({

        full_name:"",

        email:"",

        phone:"",

        date_of_birth:"",

        gender:"",

        address:"",

        city:"",

        state:"",

        country:"",

        customer_type:"Retail",

        preferred_sales_channel:"Retail Store",

        status:"Active"

    });

    useEffect(() => {

        if (initialData) {
    
            setForm({
    
                full_name: initialData.full_name || "",
    
                email: initialData.email || "",
    
                phone: initialData.phone || "",
    
                date_of_birth: initialData.date_of_birth || "",
    
                gender: initialData.gender || "",
    
                address: initialData.address || "",
    
                city: initialData.city || "",
    
                state: initialData.state || "",
    
                country: initialData.country || "",
    
                customer_type: initialData.customer_type || "Retail",
    
                preferred_sales_channel:
    
                    initialData.preferred_sales_channel || "Retail Store",
    
                status: initialData.status || "Active"
    
            });
    
        }
    
        else{
    
            setForm({
    
                full_name:"",
    
                email:"",
    
                phone:"",
    
                date_of_birth:"",
    
                gender:"",
    
                address:"",
    
                city:"",
    
                state:"",
    
                country:"",
    
                customer_type:"Retail",
    
                preferred_sales_channel:"Retail Store",
    
                status:"Active"
    
            });
    
        }
    
    }, [initialData]);

    const handleChange=(

        e:React.ChangeEvent<HTMLInputElement|HTMLSelectElement>

    )=>{

        setForm({

            ...form,

            [e.target.name]:e.target.value

        });

    };

    if(!open){

        return null;

    }

    return(

        <div className="modal-overlay">

            <div className="modal">

                <h2>

                    {initialData ? "Edit Customer":"Add Customer"}

                </h2>

                <input
                    name="full_name"
                    placeholder="Full Name"
                    value={form.full_name}
                    onChange={handleChange}
                />

                <input
                    name="email"
                    placeholder="Email"
                    value={form.email}
                    onChange={handleChange}
                />

                <input
                    name="phone"
                    placeholder="Phone"
                    value={form.phone}
                    onChange={handleChange}
                />

                <input
                    type="date"
                    name="date_of_birth"
                    value={form.date_of_birth}
                    onChange={handleChange}
                />

                <select
                    name="gender"
                    value={form.gender}
                    onChange={handleChange}
                >

                    <option value="">

                        Gender

                    </option>

                    <option>

                        Male

                    </option>

                    <option>

                        Female

                    </option>

                </select>

                <input
                    name="address"
                    placeholder="Address"
                    value={form.address}
                    onChange={handleChange}
                />

                <input
                    name="city"
                    placeholder="City"
                    value={form.city}
                    onChange={handleChange}
                />

                <input
                    name="state"
                    placeholder="State"
                    value={form.state}
                    onChange={handleChange}
                />

                <input
                    name="country"
                    placeholder="Country"
                    value={form.country}
                    onChange={handleChange}
                />

                <select
                    name="customer_type"
                    value={form.customer_type}
                    onChange={handleChange}
                >

                    <option>

                        Retail

                    </option>

                    <option>

                        Wholesale

                    </option>

                    <option>

                        Corporate

                    </option>

                </select>

                <select
                    name="preferred_sales_channel"
                    value={form.preferred_sales_channel}
                    onChange={handleChange}
                >

                    <option>

                        Retail Store

                    </option>

                    <option>

                        Online

                    </option>

                    <option>

                        Marketplace

                    </option>

                </select>

                <select
                    name="status"
                    value={form.status}
                    onChange={handleChange}
                >

                    <option>

                        Active

                    </option>

                    <option>

                        Inactive

                    </option>

                </select>

                <div className="modal-buttons">

                    <button

                        onClick={async()=>{
                    
                            await onSubmit(form);
                    
                        }}
                    
                    >
                    
                        Save
                    
                    </button>

                    <button
                        onClick={onClose}
                    >

                        Cancel

                    </button>

                </div>

            </div>

        </div>

    );

}

export default CustomerForm;