from fastapi import APIRouter

from src.authentication import auth_router
from src.core.enums import AppPaths, RouteTags
from src.providers import providers_router
from src.users import users_router

router = APIRouter()

router.include_router(
    router=auth_router,
    prefix=AppPaths.AUTHENTICATION,
    tags=(RouteTags.AUTH,),
)
router.include_router(
    router=users_router,
    prefix=AppPaths.USERS,
    tags=(RouteTags.USERS,),
)
router.include_router(
    router=providers_router,
    prefix=AppPaths.PROVIDERS,
    tags=(RouteTags.PROVIDERS,),
)
