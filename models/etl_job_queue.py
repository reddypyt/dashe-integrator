from sqlalchemy import Column, Boolean, DateTime, Float, Identity, Integer, PrimaryKeyConstraint, SmallInteger, String, text
from sqlalchemy.orm import declarative_base, synonym
from . import Base
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, 'mssql')
def ms_utcnow(element, compiler, **kw):
    return "GETUTCDATE()"


class uniqueid(expression.FunctionElement):
    type = UNIQUEIDENTIFIER()


@compiles(uniqueid, 'mssql')
def ms_utcnow(element, compiler, **kw):
    return "newid()"


class EtljobQueue(Base):
    __tablename__ = 'ETL_JOB_QUEUE'
    __table_args__ = (
        PrimaryKeyConstraint(
            'QUEUE_ID', name='PK__ETL_JOB___B3E8C3C27FF1DFB6'),
        {'schema': 'dbo'}
    )

    QUEUE_ID = Column(Integer, Identity(start=1, increment=1))
    QUEUE_ENTRY_DATE = Column(
        DateTime, nullable=False, server_default=utcnow())
    QUEUE_ENTRY_SOURCE = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    QUEUE_PICKUP_DATE = Column(DateTime)
    STATUS = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    BATCH_ID = Column(UNIQUEIDENTIFIER, server_default=uniqueid())

    CYCLE_ID = Column(Integer)
    CYCLE_DESC = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CLIENT_ID = Column(SmallInteger)
    CLIENT_DESCR = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    ETL_CHAIN_ID = Column(Integer)
    ETL_LEVEL_ID = Column(Integer)
    ETL_DATA_FLOW_ID = Column(Integer)
    COMMENTS = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    ACTIVE_FLAG = Column(Boolean)
    HANDSHAKE_FLAG = Column(Boolean)
    UPDATE_DATE = Column(DateTime, server_default=utcnow())
    UPDATE_USER_ID = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PROVIDER_ID = Column(Integer)
    APPLICATION = Column(String(64, 'SQL_Latin1_General_CP1_CI_AS'))
    SERVICE_ID = Column(Integer)
    id = synonym('QUEUE_ID')
