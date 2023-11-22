from sqlalchemy import Column, Integer, String, DateTime, and_, \
    or_, INT, VARCHAR, UniqueConstraint, Boolean, Numeric, BigInteger, ForeignKey, Table,  func, Float, Index, UUID
from sqlalchemy.orm import relationship
from zing_product_backend.models.auth import User
from zing_product_backend.app_db.connections import Base
from zing_product_backend.core import common
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

