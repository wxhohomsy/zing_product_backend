from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, DateTime, and_, \
    or_, INT, VARCHAR, UniqueConstraint, Boolean, Numeric, BigInteger, ForeignKey, func, Table, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import Enum
from zing_product_backend.app_db.connections import Base
from zing_product_backend.core.product_containment import containment_constants
from zing_product_backend.core import common
from zing_product_backend.models import auth
from sqlalchemy.dialects.postgresql import UUID, BIGINT


class RequestRecord(Base):
    __tablename__ = 'request_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    from_ip = Column(VARCHAR(), nullable=False)
    from_user = Column(VARCHAR(), nullable=True)
    method = Column(VARCHAR(), nullable=False)
    request_url = Column(VARCHAR(), nullable=False)
    request_body = Column(JSONB(), nullable=True)
    request_headers = Column(JSONB(), nullable=True)
    response_status = Column(Integer(), nullable=True)
