import asyncio
import logging
import os
import sys

import asyncpg
import numpy as np
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import Config

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("fastapi_ml_template")

LOGGER.info(os.getenv("POSTGRES_USER"))

config = Config()


@pytest.mark.asyncio
async def test_create_async_table() -> None:
    LOGGER.info("Connecting to Postgres...")

    conn = await asyncpg.connect(
        user=config.postgres_user,
        password=config.postgres_password,
        database=config.postgres_db,
        host=config.postgres_host,
    )

    LOGGER.info("Connection established")

    await conn.execute(
        """
        DROP TABLE IF EXISTS test_async_write
        """
    )

    await conn.execute(
        """
        CREATE TABLE test_async_write(
            id serial PRIMARY KEY,
            x1 float,
            x2 float
        )
    """
    )

    LOGGER.info("Successfully created test_async_write table")

    await conn.close()

    LOGGER.info("Connection closed")


@pytest.mark.asyncio
async def test_write_data_async():
    conn = await asyncpg.connect(
        user=config.postgres_user,
        password=config.postgres_password,
        database=config.postgres_db,
        host=config.postgres_host,
    )

    data = np.random.normal(size=(1_000_000, 2))
    data_to_insert = [tuple(row) for row in data]

    insert_query = "INSERT INTO test_async_write (x1, x2) VALUES ($1, $2)"

    LOGGER.info(f"Writing {len(data_to_insert)} rows...")

    await conn.executemany(insert_query, data_to_insert)

    LOGGER.info("Finished writing")

    await conn.close()


asyncio.run(test_create_async_table())
asyncio.run(test_write_data_async())
