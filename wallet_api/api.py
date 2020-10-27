from typing import Optional, Tuple

from flask import Blueprint, current_app, g, jsonify, Response, request
from flask_httpauth import HTTPBasicAuth
import sqlite3
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash

from wallet_api.db import get_db


auth = HTTPBasicAuth()
bp = Blueprint(
    "wallet", __name__, url_prefix="/wallet", static_folder="static"
)


@auth.verify_password
def verify_password(username: str, password: str) -> bool:
    """
    Verify the provided user credentials.

    Args:
        username -- the username of the user to be verified.
        password -- their password.

    Returns:
        True/False for the validity of the credentials
    """
    db = get_db()
    sql = "SELECT id, password FROM users WHERE username = ?"
    result = db.execute(sql, (username,)).fetchone()

    if result is not None:
        g.user = result["id"]

        if check_password_hash(result["password"], password):
            return True

    current_app.logger.debug(f"Unauthorised access attempt by {username}")
    return False


@bp.route("/transfer", methods=["POST"])
@auth.login_required
def transfer() -> Tuple[dict, Optional[int]]:
    """
    Handle requests to transfer funds, expects to receive JSON data
    containing the receiver's username and the amount, i.e.:

    {
        "receiver": "john",
        "amount": 100
    }

    The sender is the currently authenticated user.
    """
    if request.json.keys() < {"amount", "receiver"}:
        raise BadRequest(
            "Invalid request, please provide both receiver and amount"
        )

    receiver_username = request.json["receiver"]
    amount = request.json["amount"]

    db = get_db()
    sql = "SELECT id FROM users WHERE username = ?"
    result = db.execute(sql, (receiver_username,)).fetchone()

    if result is not None:
        receiver_id = result["id"]

        # only commit or rollback all updates and ensure the sender has
        # sufficient balanace before proceeding.
        db.isolation_level = None
        c = db.cursor()
        c.execute("begin")
        try:
            sql = "SELECT balance FROM users WHERE id = ?"
            result = c.execute(sql, (g.user,)).fetchone()
            if int(result["balance"]) < amount:
                raise ValueError("Insufficient funds for transfer")

            c.execute(
                "UPDATE users SET balance = balance + ? WHERE id = ?",
                (amount, receiver_id),
            )

            c.execute(
                "UPDATE users SET balance = balance - ? WHERE id = ?",
                (amount, g.user),
            )

            c.execute(
                "INSERT INTO transactions (sender_id, receiver_id, value) "
                "VALUES (?,?,?);",
                (g.user, receiver_id, amount),
            )
            c.execute("commit")
        except sqlite3.Error as e:
            current_app.logger.error(f"Transaction failed: {e}")
            c.execute("rollback")
            return jsonify(error="Unable to complete transaction"), 500
        except ValueError:
            return jsonify(error="Insufficient funds for transfer"), 403
            c.execute("rollback")

        return jsonify(success="True")

    return jsonify(error="Invalid User Provided"), 400


@bp.route("/balance", methods=["GET"])
@auth.login_required
def balance() -> Response:
    """
    Handle balanace requests for the currently authenticated user.
    """
    db = get_db()
    sql = "SELECT balance FROM users WHERE id = ?"
    result = db.execute(sql, (g.user,)).fetchone()

    return jsonify({"balance": result["balance"]})


@bp.route("/transactions", methods=["GET"])
@auth.login_required
def transactions() -> Response:
    """
    Handle transaction requests for the currently authenticated user.
    """
    db = get_db()
    sql = (
        "SELECT "
        "transaction_timestamp, "
        "value, "
        "s.username as sender, "
        "r.username as receiver "
        "FROM transactions "
        "LEFT JOIN users s on s.id = transactions.sender_id "
        "LEFT JOIN users r on r.id = transactions.receiver_id "
        "WHERE sender_id = ? OR receiver_id = ?"
    )

    result = db.execute(sql, (g.user, g.user)).fetchall()

    transactions = {
        "transactions": [
            {
                "sender": row["sender"],
                "receiver": row["receiver"],
                "date": row["transaction_timestamp"],
                "amount": row["value"],
            }
            for row in result
        ]
    }
    return jsonify(transactions)


@bp.route("/documentation", methods=["GET"])
def documentation() -> Response:
    """
    Send the OpenAPI documentation to the client.
    """
    return bp.send_static_file("openapispec.html")
