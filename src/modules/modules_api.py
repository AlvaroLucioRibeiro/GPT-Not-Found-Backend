from fastapi import APIRouter
from routes.route_events import events_router
from routes.route_customers_me import customers_router
from routes.route_authentication import authentication_router


# -------------------- API ROUTES -------------------- #
router = APIRouter()

router.include_router(authentication_router)
router.include_router(customers_router)
router.include_router(events_router)
