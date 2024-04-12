import asyncpg
import numpy as np
import pytest
import pytest_asyncio

from app.config import Config

CONFIG = Config()


@pytest_asyncio.fixture()
async def postgres_connection():
    conn = await asyncpg.connect(
        user=CONFIG.postgres_user,
        password=CONFIG.postgres_password,
        database=CONFIG.postgres_db,
        host=CONFIG.postgres_host,
    )

    return conn


@pytest.fixture()
def fake_postgres_data():
    data = np.random.normal(size=(100_000, 2))
    data_list = [tuple(row) for row in data]

    return data_list
