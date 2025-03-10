from fastapi import APIRouter
from routes.route_authentication import authentication_router


# -------------------- API ROUTES -------------------- #
router = APIRouter()

router.include_router(authentication_router)
