from sqlalchemy import Column, Integer, String, DateTime, and_, \
    or_, INT, VARCHAR, UniqueConstraint, Boolean, Numeric, BigInteger, ForeignKey, func, Table, Index
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import Enum
from zing_product_backend.models import auth
from zing_product_backend.app_db.connections import Base
from zing_product_backend.core import common

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

containment_rule_user_table = Table(
    "containment_rule_user",
    Base.metadata,
    Column("rule_id", ForeignKey(f'{db_schema}.containment_rule.id')),
    Column("user_id", ForeignKey(f'{db_schema}.user.id')),
    Index('ix_rule_id', 'rule_id'),
    Index('ix_user_id', 'user_id'),
    schema=db_schema
)

containment_base_rule_user_table = Table(
    "containment_base_rule_user",
    Base.metadata,
    Column("base_rule_id", ForeignKey(f'{db_schema}.containment_base_rule.id')),
    Column("user_id", ForeignKey(f'{db_schema}.user.id')),
    Index('ix_base_rule_id', 'base_rule_id'),
    Index('ix_user_id', 'user_id'),
    schema=db_schema
)


class ContainmentBaseRule(Base):
    __tablename__ = "containment_base_rule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_class: common.ContainmentBaseRuleType = Column(VARCHAR(), Enum(common.ContainmentBaseRuleClass),
                                                        nullable=False, index=True)
    rule_name: common.ContainmentBaseRuleClass = Column(VARCHAR(), Enum(common.ContainmentBaseRuleClass),
                                                        nullable=False, index=True)
    rule_data = Column(JSON(), nullable=False)
    rule_sql = Column(VARCHAR(), nullable=True)
    changeable = Column(Boolean(), default=True)
    created_by = Column(VARCHAR, ForeignKey(auth.User.user_name), nullable=False, default='admin', index=True)
    created_time = Column(DateTime(), nullable=False, default=func.now())
    updated_by = Column(VARCHAR, ForeignKey(auth.User.user_name), nullable=False, default='admin', index=True)
    updated_time = Column(DateTime(), nullable=False, default=func.now(), onupdate=func.now())
    rules = relationship('ContainmentRule', secondary='containment_rule_base_rule',
                         back_populates='base_rules', lazy='selectin'
                         )
    create_users: Mapped[auth.User] = relationship(
        foreign_keys=[created_by],
        back_populates='ContainmentBaseRule', lazy='selectin', )
    update_users: Mapped[auth.User] = relationship(
        foreign_keys=[updated_by],
        back_populates='ContainmentBaseRule', lazy='selectin',
    )


class ContainmentRule(Base):
    __tablename__ = "containment_rule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_description = Column(VARCHAR(), nullable=False)
    containment_object_type: common.ProductObjectType = Column(VARCHAR(), nullable=False)
    changeable = Column(Boolean(), default=True)
    rule_data = Column(JSON(), nullable=False)
    created_by = Column(VARCHAR, ForeignKey(auth.User.user_name), nullable=False, default='admin')
    created_time = Column(DateTime(), nullable=False, default=func.now())
    updated_by = Column(VARCHAR, ForeignKey(auth.User.user_name), nullable=False, default='admin')
    updated_time = Column(DateTime(), nullable=False, default=func.now(), onupdate=func.now())
    base_rules = relationship('ContainmentBaseRule', secondary='containment_rule_base_rule',
                              back_populates='rules', lazy='selectin')
    create_users: Mapped[auth.User] = relationship(
        foreign_keys=[created_by],
        back_populates='ContainmentRule', lazy='selectin', )
    update_users: Mapped[auth.User] = relationship(
        foreign_keys=[updated_by],
        back_populates='ContainmentBaseRule', lazy='selectin',
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
