from fastapi import APIRouter
from src.admin import admin_router
from src.core.enums import AppPaths, RouteTags
from src.parents import parents_router
from src.providers import providers_router

router = APIRouter(prefix=AppPaths.V1)


router.include_router(
    router=admin_router,
    prefix=AppPaths.ADMINS,
    tags=(RouteTags.ADMINS,),
)
router.include_router(
    router=parents_router,
    prefix=AppPaths.PARENTS,
    tags=(RouteTags.PARENTS,),
)
router.include_router(
    router=providers_router,
    prefix=AppPaths.PROVIDERS,
    tags=(RouteTags.PROVIDERS,),
)
