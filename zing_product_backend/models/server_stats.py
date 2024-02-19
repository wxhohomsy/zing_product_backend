import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, DateTime, and_, \
    or_, INT, VARCHAR, UniqueConstraint, Boolean, Numeric, BigInteger, ForeignKey, func, Table, Index
from sqlalchemy.dialects.postgresql import JSONB, BYTEA
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import Enum
from zing_product_backend.app_db.connections import Base


class RequestRecord(Base):
    __tablename__ = 'request_record'
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    request_type: str = Column(VARCHAR(), nullable=False)
    client_ip: str = Column(VARCHAR(), nullable=False)
    server_ip: str = Column(VARCHAR(), nullable=False)
    server_port: int = Column(Integer(), nullable=False)
    request_time: datetime.datetime = Column(DateTime(), nullable=False, index=True)
    state: Mapped[dict] = Column(JSONB(), nullable=False)
    duration: float = Column(Numeric(), nullable=False)
    path: str = Column(VARCHAR(), nullable=False, index=True)
    method: str = Column(VARCHAR(), nullable=False)
    scheme: str = Column(VARCHAR(), nullable=False)
    request_body: Mapped[bytes] = Column(BYTEA(), nullable=True)
    headers: dict = Column(JSONB(), nullable=True)
    user_name: str = Column(VARCHAR(), nullable=True)
    error_flag: bool = Column(Boolean(), nullable=True)
    traceback: str = Column(VARCHAR(), nullable=True)

