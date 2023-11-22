from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID,
)
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr, relationship
from sqlalchemy import VARCHAR, ForeignKey, DateTime, Boolean, Integer, String, Table, Index
from zing_product_backend.app_db.connections import Base
from sqlalchemy import Column, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, BIGINT
import uuid

db_schema = Base.__table_args__['schema']

# class UserGroup(Base):
#     __tablename__ = "user_group"
#     schema = Base.__table_args__['schema']
#     id = Column(BIGINT(), autoincrement=True, primary_key=True)
#     user_id = Column(UUID(as_uuid=True), ForeignKey(f'{schema}.user.id'))
#     group_id = Column(Integer(), ForeignKey(f'{schema}.privilege_group.id'))
#     group_name = Column(VARCHAR(), nullable=False)
#     user_name = Column(VARCHAR(), nullable=False)
#     created_by = Column(UUID(as_uuid=True), ForeignKey(f'{schema}.user.id'), nullable=False)


user_group_table = Table(
    "user_group",
    Base.metadata,
    Column("user_id", ForeignKey(f'{db_schema}.user.id')),
    Column("group_id", ForeignKey(f'{db_schema}.privilege_group.id')),
    Index('ix_user_id', 'user_id'),
    schema=db_schema,
)

rule_group_table = Table(
    "rule_group",
    Base.metadata,
    Column("rule_id", ForeignKey(f'{db_schema}.privilege_rules.id')),
    Column("group_id", ForeignKey(f'{db_schema}.privilege_group.id')),
    schema=db_schema
)


class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = Column(VARCHAR(), unique=True, nullable=False, index=True)
    # Define the relationship
    privilege_groups = relationship('PrivilegeGroup', secondary='test.user_group', back_populates='users',
                                    lazy='selectin'
                                    )
    email = Column(VARCHAR(), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )


class PrivilegeGroup(Base):
    __tablename__ = "privilege_group"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    group_name = Column(VARCHAR(), nullable=False)
    group_description = Column(VARCHAR(), nullable=True)
    created_by = Column(UUID(), ForeignKey(User.id), nullable=False)
    created_time = Column(DateTime(), nullable=False)
    # Define the relationship
    users = relationship('User', secondary=f'{db_schema}.user_group', back_populates='privilege_groups',
                         lazy='selectin'
                         )
    privilege_rules = relationship('PrivilegeRules', secondary=rf'{db_schema}.rule_group',
                                   back_populates='privilege_groups',
                                   lazy='selectin'
                                   )
    group_deleted = Column(Boolean(), nullable=False, default=False)


class PrivilegeRules(Base):
    __tablename__ = "privilege_rules"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    rule_name = Column(VARCHAR(), nullable=False, unique=True, index=True)
    is_active = Column(Boolean(), nullable=False, default=True)
    rule_description = Column(VARCHAR(), nullable=True)
    privilege_groups = relationship('PrivilegeGroup', secondary=rf'{db_schema}.rule_group',
                                    back_populates='privilege_rules', lazy='selectin')


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    @declared_attr
    def user_id(cls) -> Mapped[GUID]:  # redefined for schema matching
        return mapped_column(
            GUID, ForeignKey(User.id, ondelete="cascade"), nullable=False
        )


if __name__ == "__main__":
    from zing_product_backend.app_db.connections import AppSession
    with AppSession() as s:
        user = User(user_name='admin', email='dasda@dsad.com', hashed_password='dasdasd')
        s.add(user)
        s.flush()
        group = PrivilegeGroup(group_name='admin', created_by=user.id, created_time='2021-01-01')
        user.privilege_groups.append(group)
        s.commit()
