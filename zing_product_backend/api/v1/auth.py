from fastapi import Depends, FastAPI
from fastapi import APIRouter
from zing_product_backend.core.security.users import fastapi_users
from zing_product_backend.core.security.auth_backend import auth_backend
from zing_product_backend.core.security import schema,  users, security_api

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # responses={401: {"description": "auth error"}},
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/db", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(schema.UserRead, schema.UserCreate),
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(schema.UserRead),
    tags=["auth"],
)
router.include_router(
    security_api.user_info_router,
    prefix="/users",
    tags=["auth"],
)

router.include_router(
    security_api.privilege_router,
    prefix="/privilege",
    tags=["auth"],
)
