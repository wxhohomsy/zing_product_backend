from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.schema import  Column, ForeignKey
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID,
)
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy
from zing_product_backend.app_db.connections import Base, app_db_engine, app_async_engine, AsyncSession


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    @declared_attr
    def user_id(cls) -> Mapped[GUID]:   # redefined for schema matching
        return mapped_column(
            GUID, ForeignKey(User.id, ondelete="cascade"), nullable=False
        )




