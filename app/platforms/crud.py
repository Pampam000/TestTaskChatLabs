from asyncpg import Connection, Record

from app.db import with_connection


@with_connection
async def get_all_platform_names(conn: Connection) -> list[Record]:
    return await conn.fetch("SELECT * FROM Platform;")
