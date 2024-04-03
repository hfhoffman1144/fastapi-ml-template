import logging

import psycopg2

from config import Config

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

postgres_config = Config()

conn = psycopg2.connect(
    dbname=postgres_config.postgres_db,
    user=postgres_config.postgres_user,
    password=postgres_config.postgres_password,
    host=postgres_config.postgres_host,
)

cur = conn.cursor()

try:
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        age INT
    )
    """
    )
    LOGGER.info("test_table created successfully")

    cur.execute("INSERT INTO test_table (name, age) VALUES (%s, %s)", ("Alice", 30))
    cur.execute("INSERT INTO test_table (name, age) VALUES (%s, %s)", ("Bob", 25))
    conn.commit()
    LOGGER.info("Data inserted successfully into test_table")

    cur.execute("SELECT * FROM test_table")
    rows = cur.fetchall()
    LOGGER.info("Data selected from test_table:")
    for row in rows:
        LOGGER.info(f"ID = {row[0]}, NAME = {row[1]}, AGE = {row[2]}")

    cur.execute("DROP TABLE IF EXISTS test_table")
    conn.commit()
    LOGGER.info("Dropped test_table")

finally:
    cur.close()
    conn.close()
    LOGGER.info("Database connection closed")
