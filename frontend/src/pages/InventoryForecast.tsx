import {
    useEffect,
    useState
} from "react";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

import {
    getInventoryForecast,
    getProductInventoryRecommendation
} from "../services/inventoryForecastService";

import "../styles/inventoryForecast.css";


interface ForecastProduct {

    product_id: number;

    product_name: string;

    sku: string;

    category_name?: string;

    current_stock: number;

    available_stock: number;

    average_daily_sales: number;

    forecasted_demand: number;

    days_of_stock_remaining:
        number | null;

    lead_time_days: number;

    safety_stock: number;

    reorder_point: number;

    recommended_reorder_quantity: number;

    stock_risk: string;

    recommendation: string;

    reorder_required: boolean;
}


interface Summary {

    total_products: number;

    products_requiring_reorder: number;

    stockout_risk_products: number;

    overstocked_products: number;

    healthy_products: number;
}


function InventoryForecast() {

    const [products, setProducts] =
        useState<ForecastProduct[]>([]);

    const [summary, setSummary] =
        useState<Summary>({
            total_products: 0,
            products_requiring_reorder: 0,
            stockout_risk_products: 0,
            overstocked_products: 0,
            healthy_products: 0
        });


    const [selectedProduct, setSelectedProduct] =
        useState<ForecastProduct | null>(null);


    const [loading, setLoading] =
        useState(false);


    const [error, setError] =
        useState("");


    const [forecastDays, setForecastDays] =
        useState(30);


    const [riskFilter, setRiskFilter] =
        useState("");


    const [reorderFilter, setReorderFilter] =
        useState("");


    const [sortBy, setSortBy] =
        useState("");


    // =====================================================
    // Load Forecast
    // =====================================================

    const loadForecast = async () => {

        try {

            setLoading(true);

            setError("");

            const params: any = {

                forecast_days:
                    forecastDays,

            };


            if (riskFilter) {

                params.stock_risk =
                    riskFilter;

            }


            if (reorderFilter !== "") {

                params.reorder_required =
                    reorderFilter === "true";

            }


            if (sortBy) {

                params.sort_by =
                    sortBy;

            }


            const response =
                await getInventoryForecast(
                    params
                );


            setProducts(
                response.data.products
            );


            setSummary(
                response.data.summary
            );

        }

        catch (err) {

            console.error(err);

            setError(
                "Failed to load inventory forecast."
            );

        }

        finally {

            setLoading(false);

        }

    };


    useEffect(() => {

        loadForecast();

    }, [
        forecastDays,
        riskFilter,
        reorderFilter,
        sortBy
    ]);


    // =====================================================
    // Product Selection
    // =====================================================

    const handleProductSelect =
        async (
            product: ForecastProduct
        ) => {

            try {

                const response =
                    await getProductInventoryRecommendation(
                        product.product_id,
                        {
                            forecast_days:
                                forecastDays
                        }
                    );


                setSelectedProduct(
                    response.data
                );

            }

            catch (err) {

                console.error(err);

                setError(
                    "Failed to load product recommendation."
                );

            }

        };


    return (

        <>

            <Sidebar />

            <Navbar />


            <div className="inventory-forecast">

                <div className="inventory-forecast-header">

                    <h2>
                        Inventory Forecast
                    </h2>

                    <p>
                        Forecast demand and identify
                        inventory replenishment requirements.
                    </p>

                </div>


                {/* =================================================
                    Summary Cards
                ================================================= */}

                <div className="forecast-summary">

                    <div className="forecast-card">

                        <h3>
                            Products
                        </h3>

                        <strong>
                            {summary.total_products}
                        </strong>

                    </div>


                    <div className="forecast-card reorder">

                        <h3>
                            Requiring Reorder
                        </h3>

                        <strong>
                            {
                                summary
                                    .products_requiring_reorder
                            }
                        </strong>

                    </div>


                    <div className="forecast-card risk">

                        <h3>
                            Stockout Risk
                        </h3>

                        <strong>
                            {
                                summary
                                    .stockout_risk_products
                            }
                        </strong>

                    </div>


                    <div className="forecast-card overstock">

                        <h3>
                            Overstock
                        </h3>

                        <strong>
                            {
                                summary
                                    .overstocked_products
                            }
                        </strong>

                    </div>


                    <div className="forecast-card healthy">

                        <h3>
                            Healthy
                        </h3>

                        <strong>
                            {
                                summary
                                    .healthy_products
                            }
                        </strong>

                    </div>

                </div>


                {/* =================================================
                    Filters
                ================================================= */}

                <div className="forecast-filters">

                    <select
                        value={forecastDays}
                        onChange={(e) =>
                            setForecastDays(
                                Number(e.target.value)
                            )
                        }
                    >

                        <option value={7}>
                            Next 7 Days
                        </option>

                        <option value={30}>
                            Next 30 Days
                        </option>

                        <option value={90}>
                            Next 90 Days
                        </option>

                    </select>


                    <select
                        value={riskFilter}
                        onChange={(e) =>
                            setRiskFilter(
                                e.target.value
                            )
                        }
                    >

                        <option value="">
                            All Stock Risks
                        </option>

                        <option value="Out of Stock">
                            Out of Stock
                        </option>

                        <option value="Stockout Risk">
                            Stockout Risk
                        </option>

                        <option value="Low Stock">
                            Low Stock
                        </option>

                        <option value="Healthy">
                            Healthy
                        </option>

                        <option value="Overstock">
                            Overstock
                        </option>

                    </select>


                    <select
                        value={reorderFilter}
                        onChange={(e) =>
                            setReorderFilter(
                                e.target.value
                            )
                        }
                    >

                        <option value="">
                            Reorder Required
                        </option>

                        <option value="true">
                            Yes
                        </option>

                        <option value="false">
                            No
                        </option>

                    </select>


                    <select
                        value={sortBy}
                        onChange={(e) =>
                            setSortBy(
                                e.target.value
                            )
                        }
                    >

                        <option value="">
                            Sort By
                        </option>

                        <option value="current_stock">
                            Current Stock
                        </option>

                        <option value="forecasted_demand">
                            Forecasted Demand
                        </option>

                        <option value="days_remaining">
                            Days Remaining
                        </option>

                        <option value="recommended_quantity">
                            Recommended Quantity
                        </option>

                        <option value="risk">
                            Risk Level
                        </option>

                    </select>

                </div>


                {/* =================================================
                    Error
                ================================================= */}

                {error && (

                    <div className="forecast-error">

                        {error}

                    </div>

                )}


                {/* =================================================
                    Loading
                ================================================= */}

                {loading ? (

                    <div className="forecast-loading">

                        Loading inventory forecast...

                    </div>

                ) : products.length === 0 ? (

                    <div className="forecast-empty">

                        No inventory forecast data available.

                    </div>

                ) : (

                    <table className="forecast-table">

                        <thead>

                            <tr>

                                <th>Product</th>

                                <th>SKU</th>

                                <th>Current Stock</th>

                                <th>Average Daily Sales</th>

                                <th>Forecasted Demand</th>

                                <th>Days Remaining</th>

                                <th>Reorder Point</th>

                                <th>Recommended Quantity</th>

                                <th>Risk</th>

                                <th>Recommendation</th>

                            </tr>

                        </thead>


                        <tbody>

                            {products.map(
                                (product) => (

                                    <tr
                                        key={
                                            product.product_id
                                        }

                                        onClick={() =>
                                            handleProductSelect(
                                                product
                                            )
                                        }
                                    >

                                        <td>
                                            {
                                                product.product_name
                                            }
                                        </td>

                                        <td>
                                            {product.sku}
                                        </td>

                                        <td>
                                            {
                                                product.current_stock
                                            }
                                        </td>

                                        <td>
                                            {
                                                product.average_daily_sales
                                            }
                                        </td>

                                        <td>
                                            {
                                                product.forecasted_demand
                                            }
                                        </td>

                                        <td>

                                            {
                                                product.days_of_stock_remaining
                                                    ?? "N/A"
                                            }

                                        </td>

                                        <td>
                                            {
                                                product.reorder_point
                                            }
                                        </td>

                                        <td>

                                            <strong>

                                                {
                                                    product
                                                        .recommended_reorder_quantity
                                                }

                                            </strong>

                                        </td>

                                        <td>

                                            <span
                                                className={
                                                    `risk-${product.stock_risk
                                                        .toLowerCase()
                                                        .replaceAll(
                                                            " ",
                                                            "-"
                                                        )}`
                                                }
                                            >

                                                {
                                                    product.stock_risk
                                                }

                                            </span>

                                        </td>

                                        <td>
                                            {
                                                product.recommendation
                                            }
                                        </td>

                                    </tr>

                                )
                            )}

                        </tbody>

                    </table>

                )}


                {/* =================================================
                    Recommendation Comparison Panel
                ================================================= */}

                {selectedProduct && (

                    <div className="recommendation-panel">

                        <h2>
                            Recommendation Comparison
                        </h2>


                        <h3>

                            {
                                selectedProduct
                                    .product_name
                            }

                        </h3>


                        <table>

                            <thead>

                                <tr>

                                    <th>Metric</th>

                                    <th>Current</th>

                                    <th>Recommended</th>

                                </tr>

                            </thead>


                            <tbody>

                                <tr>

                                    <td>Stock</td>

                                    <td>
                                        {
                                            selectedProduct
                                                .current_stock
                                        }
                                    </td>

                                    <td>
                                        {
                                            selectedProduct
                                                .current_stock +
                                            selectedProduct
                                                .recommended_reorder_quantity
                                        }
                                    </td>

                                </tr>


                                <tr>

                                    <td>Daily Demand</td>

                                    <td>
                                        {
                                            selectedProduct
                                                .average_daily_sales
                                        }
                                    </td>

                                    <td>
                                        {
                                            selectedProduct
                                                .average_daily_sales
                                        }
                                    </td>

                                </tr>


                                <tr>

                                    <td>Reorder Point</td>

                                    <td>
                                        {
                                            selectedProduct
                                                .reorder_point
                                        }
                                    </td>

                                    <td>
                                        {
                                            selectedProduct
                                                .reorder_point
                                        }
                                    </td>

                                </tr>


                                <tr>

                                    <td>Safety Stock</td>

                                    <td>
                                        {
                                            selectedProduct
                                                .safety_stock
                                        }
                                    </td>

                                    <td>
                                        {
                                            selectedProduct
                                                .safety_stock
                                        }
                                    </td>

                                </tr>

                            </tbody>

                        </table>


                        <div className="recommendation-action">

                            {
                                selectedProduct
                                    .recommendation
                            }

                        </div>

                    </div>

                )}

            </div>

        </>

    );

}


export default InventoryForecast;