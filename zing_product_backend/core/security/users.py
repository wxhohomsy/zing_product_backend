import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, exceptions, models
from zing_product_backend.core.security import schema
from zing_product_backend.models import auth
from zing_product_backend.core.security import auth_backend
from zing_product_backend.app_db.connections import Base, get_async_session
from zing_product_backend.core.security import crud
from zing_product_backend.core.security.security_utils import get_rules_from_user
from zing_product_backend.core.common import RuleName
from zing_product_backend.core.common import ErrorMessages
SECRET = "SECRET12EDASDSFDAS%JFDS.DFSFs^%21"


class UserManager(UUIDIDMixin, BaseUserManager[schema.User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    user_db: crud.ZingUserDatabase

    async def authenticate(
            self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[models.UP]:
        """
        Authenticate and return a user following an user_name and a password.

        Will automatically upgrade password hash if necessary.

        :param credentials: The user credentials.
        """
        try:
            user = await self.get_by_username(credentials.username)
        except exceptions.UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})
        return user

    async def create(
            self,
            user_create: schema.UserCreate,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)
        await self.on_after_register(created_user, request)

        return created_user

    async def get_by_username(self, username: str) -> schema.User:
        """
        Get a user by e-mail.

        :param username like 'E00100'.
        :raises UserNotExists: The user does not exist.
        :return: A user.
        """
        user = await self.user_db.get_by_user_name(username)

        if user is None:
            raise exceptions.UserNotExists()
        return user

    async def on_after_register(self, user: schema.User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: schema.User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: schema.User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield crud.ZingUserDatabase(session, user_table=auth.User)


async def get_user_manager(user_db: crud.ZingUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[schema.User, uuid.UUID](get_user_manager, [auth_backend.auth_backend])
current_active_user = fastapi_users.current_user(active=True)


async def current_admin_user(user=Depends(current_active_user)) -> auth.User:
    user_rules = get_rules_from_user(user)
    if any([RuleName.ADMIN in user_rules, RuleName.IMS_DEV in user_rules]):
        return user

    else:
        raise HTTPException(status_code=403, detail=ErrorMessages.INSUFFICIENT_PRIVILEGE)