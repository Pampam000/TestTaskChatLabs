from asyncpg import Connection, Record

from app.db import with_connection


@with_connection
async def get_user_by_id(conn: Connection, user_id: int) -> Record:
    return await conn.fetchrow("SELECT * FROM Users where id = $1;",
                               user_id)


@with_connection
async def insert_user(conn: Connection, user_id: int, username: str):
    await conn.execute(
        "INSERT INTO users (id, username) values($1, $2)",
        user_id, username)


@with_connection
async def update_balance(conn: Connection, user_id: int, balance: int):
    await conn.execute(
        "UPDATE Users SET balance = balance + $1 WHERE id = $2",
        balance, user_id)


@with_connection
async def get_balance(conn: Connection, user_id: int) -> Record:
    return await conn.fetchrow("SELECT balance FROM Users WHERE id = $1",
                               user_id)


@with_connection
async def get_admins(conn: Connection) -> list[Record]:
    return await conn.fetch("SELECT * FROM Users WHERE is_admin = TRUE")


@with_connection
async def get_all_users_except_sender(conn: Connection, user_id: int) \
        -> list[Record]:
    return await conn.fetch("SELECT * FROM Users WHERE id != $1", user_id)
