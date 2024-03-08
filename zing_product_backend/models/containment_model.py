from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, DateTime, and_, \
    or_, INT, VARCHAR, UniqueConstraint, Boolean, Numeric, BigInteger, ForeignKey, func, Table, Index, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import Enum
from zing_product_backend.app_db.connections import Base
from zing_product_backend.core.product_containment import containment_constants
from zing_product_backend.core import common
from zing_product_backend.models import auth_model
from sqlalchemy.dialects.postgresql import UUID, BIGINT
import datetime


db_schema = Base.__table_args__['schema']

containment_rule_base_rule_table = Table(
    "containment_rule_base_rule",
    Base.metadata,
    Column("base_rule_id", ForeignKey(f'{db_schema}.containment_base_rule.id')),
    Column("rule_id", ForeignKey(f'{db_schema}.containment_rule.id')),
    Index('ix_base_rule_id', 'base_rule_id'),
    Index('ix_rule_id', 'rule_id'),
    schema=db_schema
)


class ContainmentBaseRule(Base):
    __tablename__ = "containment_base_rule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_class: containment_constants.ContainmentBaseRuleClass = Column(
        VARCHAR(),
        Enum(
            containment_constants.ContainmentBaseRuleClass),
        nullable=False, index=True)
    rule_name: str = Column(VARCHAR(), nullable=False, index=True, unique=True)
    virtual_factory: common.VirtualFactory = Column(VARCHAR(), nullable=False)
    rule_data = Column(JSONB(), nullable=False)
    rule_sql = Column(VARCHAR(), nullable=True)
    containment_object_type: common.ProductObjectType = Column(VARCHAR(), nullable=False)
    description = Column(VARCHAR(), nullable=False)
    changeable = Column(Boolean(), default=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey(auth_model.User.id), nullable=False, default='admin', index=True)
    created_time = Column(DateTime(), nullable=False, default=func.now())
    updated_by = Column(UUID(as_uuid=True), ForeignKey(auth_model.User.id), nullable=False, default='admin', index=True)
    updated_time = Column(DateTime(), nullable=False, default=func.now(), onupdate=func.now())
    rules = relationship('ContainmentRule', secondary=containment_rule_base_rule_table,
                         back_populates='base_rules', lazy='selectin'
                         )
    created_user = relationship(
        "User",  # Replace "User" with the actual class name of the User model
        foreign_keys=[created_by],
        primaryjoin="User.id == ContainmentBaseRule.created_by",  # Explicitly define the join condition
        lazy='selectin'
    )

    updated_user = relationship(
        "User",  # Replace "User" with the actual class name of the User model
        foreign_keys=[updated_by],
        primaryjoin="User.id == ContainmentBaseRule.updated_by",  # Explicitly define the join condition
        lazy='selectin'
    )


class ContainmentRule(Base):
    __tablename__ = "containment_rule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_name = Column(VARCHAR(), nullable=False, index=True)
    rule_description = Column(VARCHAR(), nullable=False)
    changeable = Column(Boolean(), default=True)
    rule_data = Column(JSONB(), nullable=False)
    containment_object_type: common.ProductObjectType = Column(VARCHAR(), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey(auth_model.User.id), nullable=False, default='admin')
    created_time = Column(DateTime(), nullable=False, default=func.now())
    updated_by = Column(UUID(as_uuid=True), ForeignKey(auth_model.User.id), nullable=False, default='admin')
    updated_time = Column(DateTime(), nullable=False, default=func.now(), onupdate=func.now())

    base_rules = relationship('ContainmentBaseRule', secondary=containment_rule_base_rule_table,
                              back_populates='rules', lazy='selectin')
    created_user = relationship(
        "User",  # Replace "User" with the actual class name of the User model
        foreign_keys=[created_by],
        primaryjoin="User.id == ContainmentRule.created_by",  # Explicitly define the join condition
        lazy='selectin'
    )

    updated_user = relationship(
        "User",  # Replace "User" with the actual class name of the User model
        foreign_keys=[updated_by],
        primaryjoin="User.id == ContainmentRule.updated_by",  # Explicitly define the join condition
        lazy='selectin'
    )


class ContainmentRuleStats(Base):
    __tablename__ = "containment_stats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    object_type: common.ProductObjectType = Column(VARCHAR(), nullable=True)
    object_id = Column(VARCHAR(), nullable=True)
    rule_id = Column(Integer, ForeignKey(ContainmentRule.id), nullable=False)
    rule = relationship(ContainmentRule)
    containment_time = Column(DateTime(), nullable=False, default=func.now())
    time_cost = Column(Numeric(), nullable=False)


class OOCRules(Base):
    __tablename__ = 'ooc_rules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    containment_rule_id = Column(Integer, ForeignKey(ContainmentRule.id), nullable=False, index=True)
    spec_id: Mapped[str] = Column(VARCHAR(), nullable=False, index=True)
    lower_limit = Column(Float)
    upper_limit = Column(Float)
    create_time: Mapped[datetime.datetime] = Column(DateTime, default=func.now(), nullable=False)
    create_user_name = Column(VARCHAR(), ForeignKey(auth_model.User.user_name), nullable=False)
    updated_time = Column(DateTime(), nullable=False, default=func.now(), onupdate=func.now())
    updated_user_name = Column(VARCHAR(), ForeignKey(auth_model.User.user_name), nullable=False)
    rule_delete_flag: Mapped[str] = Column(Boolean(), default=False)
