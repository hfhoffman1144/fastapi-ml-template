import logging

import pytest

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("fastapi_ml_template")


@pytest.mark.asyncio
async def test_create_async_table(postgres_connection) -> None:
    await postgres_connection.execute(
        """
        DROP TABLE IF EXISTS test_async_write
        """
    )

    await postgres_connection.execute(
        """
        CREATE TABLE test_async_write(
            id serial PRIMARY KEY,
            x1 float,
            x2 float
        )
    """
    )

    LOGGER.info("Successfully created test_async_write table")

    await postgres_connection.close()

    LOGGER.info("Connection closed")


@pytest.mark.asyncio
async def test_write_data_async(postgres_connection, fake_postgres_data):
    insert_query = "INSERT INTO test_async_write (x1, x2) VALUES ($1, $2)"

    LOGGER.info(f"Writing {len(fake_postgres_data)} rows...")

    await postgres_connection.executemany(insert_query, fake_postgres_data)

    LOGGER.info("Finished writing")

    await postgres_connection.close()
