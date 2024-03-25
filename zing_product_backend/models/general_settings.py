from sqlalchemy import Column, Integer, String, DateTime, and_, \
    or_, INT, VARCHAR, UniqueConstraint, Boolean, Numeric, BigInteger, ForeignKey, Table,  func, Float, Index, UUID
from sqlalchemy.orm import relationship,Mapped
from zing_product_backend.models.auth_model import User
from zing_product_backend.app_db.connections import Base
from zing_product_backend.core import common
import datetime
from .containment_model import ContainmentRule
from zing_product_backend.models import auth_model

db_schema = Base.__table_args__['schema']


mat_group_table = Table(
    "mat_group",
    Base.metadata,
    Column("mat_id", ForeignKey(f'{db_schema}.mat_def.id')),
    Column("mat_group_id", ForeignKey(f'{db_schema}.mat_group_def.id')),
    Index('ix_mat_id', 'mat_id'),
    Index('ix_mat_group_id', 'mat_group_id'),
    schema=db_schema
)


class MatGroupDef(Base):
    __tablename__ = 'mat_group_def'
    id = Column(Integer, primary_key=True)
    group_name = Column(VARCHAR(), nullable=False, index=True)
    group_type: common.MatGroupType = Column(VARCHAR(), nullable=False, comment='group defined for different purpose')
    group_description = Column(VARCHAR(), nullable=True)
    created_by = Column(VARCHAR(), ForeignKey(f'{db_schema}.user.user_name'), nullable=False)
    created_time = Column(DateTime(), default=func.now())
    updated_time = Column(DateTime(), default=func.now(), onupdate=func.now())
    updated_by = Column(VARCHAR(), ForeignKey(f'{db_schema}.user.user_name'), nullable=False)
    materials = relationship('MatDef', secondary=rf'{db_schema}.mat_group', back_populates='groups',
                                     lazy='selectin')


class MatDef(Base):
    __tablename__ = 'mat_def'
    id = Column(Integer, primary_key=True)
    mat_id = Column(VARCHAR(), nullable=False, index=True)
    mat_base_type: common.MatBaseType = Column(VARCHAR(), nullable=False, comment='ingot or wafering')
    mat_description = Column(VARCHAR(), nullable=True)
    mat_type = Column(VARCHAR())
    mat_grp_1 = Column(VARCHAR())
    mat_grp_2 = Column(VARCHAR())
    mat_grp_3 = Column(VARCHAR())
    mat_grp_4 = Column(VARCHAR())
    mat_grp_5 = Column(VARCHAR())
    mat_grp_6 = Column(VARCHAR())
    mat_grp_7 = Column(VARCHAR())
    mat_grp_8 = Column(VARCHAR())
    mat_cmf_1 = Column(VARCHAR())
    mat_cmf_2 = Column(VARCHAR())
    mat_cmf_3 = Column(VARCHAR())
    mat_cmf_4 = Column(VARCHAR())
    def_qty_1 = Column(Float())
    def_qty_2 = Column(Float())
    def_qty_3 = Column(Float())
    first_flow = Column(VARCHAR(), index=True)
    delete_flag = Column(Boolean(), default=False)
    created_time = Column(DateTime(), default=func.now())
    updated_time = Column(DateTime(), default=func.now(), onupdate=func.now())
    updated_by = Column(VARCHAR(), ForeignKey(f'{db_schema}.user.user_name'), nullable=False)
    groups = relationship('MatGroupDef', secondary=rf'{db_schema}.mat_group',
                          back_populates='materials', lazy='selectin')


class PullerInfo(Base):
    __tablename__ = 'puller_info'
    puller_name = Column(VARCHAR(), primary_key=True)
    puller_mes_id = Column(VARCHAR(), index=True)
    puller_mes_index = Column(Integer, index=True)
    virtual_factory: common.VirtualFactory = Column(VARCHAR())
    owner_name = Column(VARCHAR(), ForeignKey(f'{db_schema}.user.user_name'), nullable=False)
    puller_type: common.PullerType = Column(VARCHAR(), nullable=False)
    puller_description = Column(VARCHAR())
    owner = relationship(
        "User",  # Replace "User" with the actual class name of the User model
        lazy='selectin'
    )


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