from fastapi import APIRouter
from routes.route_order import orders_router
from routes.route_events import events_router
from routes.route_payments import payments_router
from routes.route_products import products_router
from routes.route_invoices import invoices_router
from routes.routes_contract import contracts_router
from routes.route_customers_me import customers_router
from routes.route_orders_items import order_items_router
from routes.route_authentication import authentication_router
from routes.route_customers_data import customers_router_data


# -------------------- API ROUTES -------------------- #
router = APIRouter()

router.include_router(authentication_router)
router.include_router(customers_router_data)
router.include_router(events_router)
router.include_router(orders_router)
router.include_router(payments_router)
router.include_router(products_router)
router.include_router(customers_router)
router.include_router(order_items_router)
router.include_router(invoices_router)
router.include_router(contracts_router)
