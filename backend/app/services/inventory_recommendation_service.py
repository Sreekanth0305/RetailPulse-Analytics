from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.demand_forecast import DemandForecast


def get_inventory_recommendations(
    db: Session,
    company_id: int
):
    """
    Generate inventory recommendations
    based on current stock and predicted demand.
    """

    forecasts = (
        db.query(DemandForecast)
        .join(Product, Product.id == DemandForecast.product_id)
        .filter(
            DemandForecast.company_id == company_id,
            Product.company_id == company_id,
            Product.status == "Active"
        )
        .all()
    )

    recommendations = []

    for forecast in forecasts:

        product = forecast.product

        stock = product.stock_quantity
        demand = float(forecast.predicted_demand)

        # -------------------------
        # Recommendation Logic
        # -------------------------

        if stock == 0:

            recommendation = "Immediate Restock Required"

        elif stock < demand:

            recommendation = "Reorder Soon"

        elif stock > demand * 2:

            recommendation = "Overstock Risk"

        else:

            recommendation = "Stock Level Healthy"

        recommendations.append({

            "product_id": product.id,

            "product_name": product.name,

            "current_stock": stock,

            "predicted_demand": demand,

            "recommendation": recommendation

        })

    return recommendations