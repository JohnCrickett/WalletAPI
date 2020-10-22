import sqlite3

import click
from werkzeug.security import generate_password_hash


def _connect_to_db(database: str) -> sqlite3.Connection:
    db_connection = sqlite3.connect(
        database,
        detect_types=sqlite3.PARSE_DECLTYPES,
    )
    db_connection.row_factory = sqlite3.Row
    return db_connection


def _add_user(
    db: sqlite3.Connection, username: str, password_hash: str, balance: int
):
    sql = "INSERT INTO users (username, password, balance) " "VALUES (?, ?, ?)"
    db.execute(sql, (username, password_hash, balance))
    db.commit()


@click.command()
@click.option(
    "--database",
    type=str,
    required=True,
    help="The database to which the user should be added.",
)
@click.option(
    "--username", type=str, required=True, help="The username to be added."
)
@click.password_option()
@click.option(
    "--balance", type=int, required=True, help="The users opening balance."
)
def main(database: str, username: str, password: str, balance: int):
    """
    Command line utility to add a user to the database.

    database -- the SQLite database file to add the user to.
    username -- the username of the user to be added.
    password -- the password of the user to be added.
    balance -- the starting balance to be set for the added user.
    """
    db = _connect_to_db(database)
    password_hash = generate_password_hash(password)
    _add_user(db, username, password_hash, balance)


if __name__ == "__main__":
    main()
