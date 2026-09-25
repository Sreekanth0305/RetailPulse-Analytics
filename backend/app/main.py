from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import Base, engine

from app.models import Company, User, RefreshToken, AuditLog, Notification

from app.models.employee import Employee
from app.models.category import Category
from app.models.product import Product
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.inventory import Inventory
from app.models.inventory_movement import InventoryMovement
from app.models.customer_purchase_summary import CustomerPurchaseSummary
from app.models.demand_forecast import DemandForecast
from app.models.forecast_history import ForecastHistory
from app.models.import_history import ImportHistory
from app.models.import_error import ImportErrorRecord

from app.routes.company_routes import router as company_router
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.employee_routes import router as employee_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.audit_routes import router as audit_router
from app.routes.category_routes import router as category_router
from app.routes.product_routes import router as product_router
from app.routes.sale_routes import router as sale_router
from app.routes.notification_routes import router as notification_router
from app.routes.inventory_routes import router as inventory_router
from app.routes.analytics_routes import router as analytics_router
from app.routes.customer_routes import router as customer_router
from app.routes.customer_profile_routes import router as customer_profile_router
from app.routes.customer_timeline_routes import router as customer_timeline_router
from app.routes.forecast_routes import router as forecast_router
from app.routes.inventory_forecast_routes import router as inventory_forecast_router
from app.routes.import_routes import router as import_router
from app.routes.report_routes import router as report_router
from app.routes.scheduled_report_routes import (router as scheduled_report_router)
from app.routes.data_quality_routes import router as data_quality_router
from app.services.scheduler_service import (
    start_scheduler,
    stop_scheduler
)


Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()

    yield

    stop_scheduler()


app = FastAPI(
    title="RetailPulse Analytics",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "RetailPulse Analytics Backend Running"
    }


app.include_router(company_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(employee_router)
app.include_router(dashboard_router)
app.include_router(audit_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(sale_router)
app.include_router(notification_router)
app.include_router(inventory_forecast_router)
app.include_router(inventory_router)
app.include_router(analytics_router)
app.include_router(customer_router)
app.include_router(customer_profile_router)
app.include_router(customer_timeline_router)
app.include_router(forecast_router)
app.include_router(import_router)
app.include_router(report_router)
app.include_router(scheduled_report_router)
app.include_router(data_quality_router)