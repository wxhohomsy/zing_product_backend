from sqlalchemy import Column, Integer, String, DateTime, and_, \
    or_, INT, VARCHAR, UniqueConstraint, Boolean, Numeric, BigInteger, ForeignKey, func, Table
from sqlalchemy.orm import relationship
from zing_product_backend.models import auth
from zing_product_backend.app_db.connections import Base
from zing_product_backend.core import common


db_schema = Base.__table_args__['schema']


containment_rule_base_rule_table = Table(
    "containment_rule_base_rule",
    Base.metadata,
    Column("base_rule_id", ForeignKey(f'{db_schema}.containment_base_rule.id')),
    Column("rule_id", ForeignKey(f'{db_schema}.containment_rule.id')),
    schema=db_schema
)


class ContainmentBaseRule(Base):
    __tablename__ = "containment_base_rule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_type: common.ContainmentBaseRuleType = Column(VARCHAR(), nullable=False)
    rule_name = Column(VARCHAR(), nullable=False)
    rule_data = Column(VARCHAR(), nullable=False)
    rules = relationship('ContainmentRule', secondary='containment_rule_base_rule',
                         back_populates='base_rules', lazy='selectin'
                         )


class ContainmentRule(Base):
    __tablename__ = "containment_rule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_description = Column(VARCHAR(), nullable=False)
    created_by = Column(VARCHAR, ForeignKey(auth.User.user_name), nullable=False, default='admin')
    created_time = Column(DateTime(), nullable=False, default=func.now())
    base_rules = relationship('ContainmentBaseRule', secondary='containment_rule_base_rule',
                              back_populates='rules', lazy='selectin')


class ContainmentRuleStats(Base):
    __tablename__ = "containment_stats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    object_type: common.ProductObjectType = Column(VARCHAR(), nullable=True)
    object_id = Column(VARCHAR(), nullable=True)
    rule_id = Column(Integer, ForeignKey(ContainmentRule.id), nullable=False)
    rule = relationship(ContainmentRule)
    containment_time = Column(DateTime(), nullable=False, default=func.now())
    time_cost = Column(Numeric(), nullable=False)
