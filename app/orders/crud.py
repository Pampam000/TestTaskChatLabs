from asyncpg import Connection

from app.db import with_connection


@with_connection
async def insert_order(conn: Connection, list_of_args: list[str]):
    await conn.execute(
        """INSERT INTO orders 
        (business_name, platform_name, min_price, max_price, phone, user_id) 
        VALUES($1, $2, $3, $4, $5, $6);""",
        *list_of_args)
