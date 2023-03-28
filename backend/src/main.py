from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse, RedirectResponse

from src.api import api_router
from src.authentication.security import admin_always_exists
from src.config import settings
from src.core.utils import change_openapi_schema
from src.db.postgres.database import check_postgres
from src.db.redis.database import check_redis

app = FastAPI(
    debug=settings.debug,
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)

app.include_router(
    router=api_router,
    prefix=settings.api_v1_prefix,
)


def custom_openapi():
    """Change status code `422` to `400` in OpenAPI scheme."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="".join(("`", app.description, "`")),
        routes=app.routes,
    )
    app.openapi_schema = change_openapi_schema(openapi_schema)
    return app.openapi_schema


app.openapi = custom_openapi

origins = [
    "http://localhost",
    "http://localhost:8008",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def bad_request_handler(request: Request, exc: RequestValidationError):
    desc = [(err["loc"][1], err["msg"]) for err in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": desc},
    )


@app.on_event("startup")
async def start_up():
    check_redis()
    await check_postgres()
    await admin_always_exists()


@app.get(
    path="/",
    deprecated=True,
)
def index(req: Request):
    return RedirectResponse(str(req.base_url) + "docs")
