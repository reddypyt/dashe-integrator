import os
from contextlib import contextmanager
from typing import Generator

import snowflake.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


PG_USER = os.environ.get('PG_USER', 'dash')
PG_PWD = os.environ.get('PG_PASSWORD', 'dash')
PG_SERVER = os.environ.get('PG_SERVER', 'postgres')
PG_PORT = os.environ.get('PG_PORT', 5432)
PG_DB = os.environ.get('PG_DB', 'dash')

DATABASE_URL = os.environ.get(
    'DATABASE_URL', f'postgresql+psycopg://{PG_USER}:{PG_PWD}@{PG_SERVER}:{PG_PORT}/{PG_DB}')
DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://')

pg_engine = create_engine(DATABASE_URL)
PG_SESSION = sessionmaker(pg_engine)

contextmanager


def get_pg_connection(autocommit: bool = True) -> Generator:
    execute_options = {}
    if autocommit is True:
        execute_options = {
            'isolation_level': 'AUTOCOMMIT'
        }

    with pg_engine.connect().execution_options(**execute_options) as pg_connection:
        yield pg_connection


@contextmanager
def get_pg_session() -> Generator:
    with PG_SESSION.begin() as pg_session:
        yield pg_session


SF_USER = os.environ.get('SF_USER')
SF_PWD = os.environ.get('SF_PWD')


@contextmanager
def get_sf_connection() -> Generator:
    with snowflake.connector.connect(
        user=SF_USER,
        password=SF_PWD,
        account='FF80747.east-us-2.azure',
        warehouse='IS_READ_ONLY_WH_XS'
    ) as sf_connection:
        yield sf_connection
