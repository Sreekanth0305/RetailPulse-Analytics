import { useEffect, useState } from "react";
import axios from "axios";

import {
  createSale,
  updateSale,
  getSaleById,
} from "../services/saleService";

interface Product {
  id: number;
  category_id: number;
  category_name: string;
  name: string;
  unit_price: number;
  stock_quantity: number;
}

interface SaleItem {
  product_id: number;
  category_id: number;
  category_name: string;

  quantity: number;

  unit_price: number;

  discount: number;

  tax: number;

  total: number;
}

interface SaleFormProps {
  saleId?: number;
  onSuccess: () => void;
}

const SaleForm = ({
  saleId,
  onSuccess,
}: SaleFormProps) => {

  const [loading, setLoading] =
    useState(false);

  const [products, setProducts] =
    useState<Product[]>([]);

  const [customerName, setCustomerName] =
    useState("");

  const [salesChannel, setSalesChannel] =
    useState("Retail Store");

  const [paymentMethod, setPaymentMethod] =
    useState("Cash");

  const [items, setItems] = useState<SaleItem[]>([
    {
      product_id: 0,
      category_id: 0,
      category_name: "",

      quantity: 1,

      unit_price: 0,

      discount: 0,

      tax: 0,

      total: 0,
    },
  ]);

  const loadProducts = async () => {
    try {
      const token = localStorage.getItem("access_token");

      const response =
        await axios.get(
          "http://127.0.0.1:8001/products/",
          {
            headers: {
              Authorization:
                `Bearer ${token}`,
            },
          }
        );

      setProducts(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  const loadSale = async () => {
    if (!saleId) return;

    try {
      const sale =
        await getSaleById(saleId);

      setCustomerName(
        sale.customer_name
      );

      setSalesChannel(
        sale.sales_channel
      );

      setPaymentMethod(
        sale.payment_method
      );

      const formattedItems =
        sale.items.map((item: any) => ({
          product_id: item.product_id,

          category_id:
            item.category_id,

          category_name:
            item.category_name,

          quantity:
            item.quantity,

          unit_price:
            item.unit_price,

          discount:
            item.discount,

          tax:
            item.tax,

          total:
            item.total,
        }));

      setItems(formattedItems);

    } catch (error) {
      console.log(error);
    }
  };

    useEffect(() => {
    loadProducts();

    if (saleId) {
      loadSale();
    }
  }, [saleId]);

   const calculateTotal = (
    item: SaleItem
  ) => {

    const subtotal =
      item.quantity *
      item.unit_price;

    return (
      subtotal -
      item.discount +
      item.tax
    );

  }; 

  const grandTotal =
    items.reduce(
      (
        sum,
        item
      ) => sum + item.total,
      0
    );

const handleProductChange = (
  index: number,
  productId: number
) => {
  const product = products.find(
    (p) => p.id === productId
  );

  if (!product) return;

  const updatedItems = [...items];

  updatedItems[index] = {
    ...updatedItems[index],
    product_id: product.id,
    category_id: product.category_id,
    category_name: product.category_name,
    unit_price: product.unit_price,
    total: calculateTotal({
      ...updatedItems[index],
      product_id: product.id,
      category_id: product.category_id,
      category_name: product.category_name,
      unit_price: product.unit_price,
    }),
  };

  setItems(updatedItems);
};

const handleItemChange = (
  index: number,
  field: keyof SaleItem,
  value: number
) => {
  const updatedItems = [...items];

  updatedItems[index] = {
    ...updatedItems[index],
    [field]: value,
  };

  updatedItems[index].total =
    calculateTotal(updatedItems[index]);

  setItems(updatedItems);
};

const addItem = () => {
  setItems([
    ...items,
    {
      product_id: 0,
      category_id: 0,
      category_name: "",
      quantity: 1,
      unit_price: 0,
      discount: 0,
      tax: 0,
      total: 0,
    },
  ]);
};

const removeItem = (index: number) => {
  const updatedItems = [...items];

  updatedItems.splice(index, 1);

  setItems(updatedItems);
};

const handleSubmit = async (
  e: React.FormEvent
) => {

  e.preventDefault();

  const payload = {

    customer_name: customerName,

    sales_channel: salesChannel,

    payment_method: paymentMethod,

    items: items.map((item) => ({
      product_id: item.product_id,
      quantity: item.quantity,
      unit_price: item.unit_price,
      discount: item.discount,
      tax: item.tax,
    })),

  };

  try {

    setLoading(true);

    if (saleId) {

      await updateSale(
        saleId,
        payload
      );

    } else {

      await createSale(
        payload
      );

    }

    onSuccess();

  } catch (error) {

    console.log(error);

  } finally {

    setLoading(false);

  }

};

return (

<form
onSubmit={handleSubmit}
className="sale-form"
>

<h2>

{saleId
? "Edit Sale"
: "Create Sale"}

</h2>

<input
type="text"
placeholder="Customer Name"
value={customerName}
onChange={(e)=>
setCustomerName(
e.target.value
)
}
required
/>

<select
value={salesChannel}
onChange={(e)=>
setSalesChannel(
e.target.value
)
}
>

<option>
Retail Store
</option>

<option>
Online Store
</option>

<option>
Marketplace
</option>

</select>

<select
value={paymentMethod}
onChange={(e)=>
setPaymentMethod(
e.target.value
)
}
>

<option>
Cash
</option>

<option>
Card
</option>

<option>
UPI
</option>

<option>
Bank Transfer
</option>

</select>

{items.map((item,index)=>(

<div
key={index}
className="sale-item"
>

    <select
value={item.product_id}
onChange={(e)=>

handleProductChange(

index,

Number(
e.target.value
)

)

}
>

<option value={0}>
Select Product
</option>

{products.map((product)=>(

<option

key={product.id}

value={product.id}

>

{product.name}

</option>

))}

</select>

<input

value={item.category_name}

readOnly

placeholder="Category"

/>

<input

type="number"

value={item.quantity}

onChange={(e)=>

handleItemChange(

index,

"quantity",

Number(e.target.value)

)

}

/>

<input

type="number"

value={item.unit_price}

readOnly

/>

<input

type="number"

value={item.discount}

onChange={(e)=>

handleItemChange(

index,

"discount",

Number(e.target.value)

)

}

/>

<input

type="number"

value={item.tax}

onChange={(e)=>

handleItemChange(

index,

"tax",

Number(e.target.value)

)

}

/>

<input

value={item.total}

readOnly

/>

<button

type="button"

onClick={()=>

removeItem(index)

}

>

Remove

</button>

</div>

))}

<button

type="button"

onClick={addItem}

>

+ Add Product

</button>

<h3>

Grand Total :

₹{grandTotal}

</h3>

<button

type="submit"

disabled={loading}

>

{

loading

?

"Saving..."

:

saleId

?

"Update Sale"

:

"Create Sale"

}

</button>

</form>

);

};

export default SaleForm;