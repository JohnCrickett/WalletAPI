from base64 import b64encode

import pytest


def _make_headers(username, password):
    credentials = b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {credentials}"}


def test_balance_invalid_user(client):
    response = client.get(
        "/wallet/balance", headers=_make_headers("invalid_user", "password")
    )
    assert response.status_code == 401


def test_balance_invalid_password(client):
    response = client.get(
        "/wallet/balance", headers=_make_headers("user1", "invalid_password")
    )
    assert response.status_code == 401


def test_balance(client):
    response = client.get(
        "/wallet/balance", headers=_make_headers("user1", "secret")
    )

    assert response.status_code == 200
    assert "balance" in response.json
    assert response.json["balance"] == 0


def test_transfer_valid_invalid_receiver(client):
    response = client.post(
        "/wallet/transfer",
        json={"receiver": "invalid_user", "amount": 50},
        headers=_make_headers("user1", "secret"),
    )

    assert response.status_code == 400
    error = response.json["error"]
    assert error == "Invalid User Provided"


def test_transfer_invalid_type(client):
    response = client.post(
        "/wallet/transfer",
        json={"receiver": "user5", "amount": "50"},
        headers=_make_headers("user4", "itsasecret"),
    )
    assert response.status_code == 400
    error = response.json["error"]
    assert (
        error
        == "Invalid amount provided, please ensure the correct type is used."
    )


def test_transfer_insufficient_funds(client):
    response = client.post(
        "/wallet/transfer",
        json={"receiver": "user5", "amount": 50},
        headers=_make_headers("user1", "secret"),
    )

    assert response.status_code == 403
    error = response.json["error"]
    assert error == "Insufficient funds for transfer"

    # Check their balance hasn't changed
    response = client.get(
        "/wallet/balance", headers=_make_headers("user1", "secret")
    )

    assert response.status_code == 200
    assert "balance" in response.json
    assert response.json["balance"] == 0


@pytest.mark.parametrize("amount", [0, -50])
def test_transfer_invalid_amount(client, amount):
    response = client.post(
        "/wallet/transfer",
        json={"receiver": "user4", "amount": amount},
        headers=_make_headers("user2", "realsecret"),
    )

    # Verify transfer not permitted
    assert response.status_code == 403
    error = response.json["error"]
    assert error == "Transfer amount must be greater than zero."

    # Verify no change to receiver's balance
    response = client.get(
        "/wallet/balance", headers=_make_headers("user4", "itsasecret")
    )
    assert response.status_code == 200
    assert "balance" in response.json
    assert response.json["balance"] == 500

    # Verify no change to sender's balance
    response = client.get(
        "/wallet/balance", headers=_make_headers("user2", "realsecret")
    )
    assert response.status_code == 200
    assert "balance" in response.json
    assert response.json["balance"] == 500

    # Verify no transaction has been recorded
    response = client.get(
        "/wallet/transactions", headers=_make_headers("user2", "realsecret")
    )
    assert response.status_code == 200
    transactions = response.json["transactions"]
    assert len(transactions) == 1
    assert transactions[0]["sender"] != "user2"
    assert transactions[0]["receiver"] != "user4"
    assert transactions[0]["amount"] != -50


def test_transfer_valid(client):
    response = client.post(
        "/wallet/transfer",
        json={"receiver": "user5", "amount": 50},
        headers=_make_headers("user4", "itsasecret"),
    )
    assert response.status_code == 200

    response = client.get(
        "/wallet/balance", headers=_make_headers("user4", "itsasecret")
    )
    assert response.status_code == 200
    assert "balance" in response.json
    assert response.json["balance"] == 450

    response = client.get(
        "/wallet/balance", headers=_make_headers("user5", "bigsecret")
    )
    assert response.status_code == 200
    assert "balance" in response.json
    assert response.json["balance"] == 50

    response = client.get(
        "/wallet/transactions", headers=_make_headers("user4", "itsasecret")
    )
    assert response.status_code == 200
    transactions = response.json["transactions"]
    assert len(transactions) == 1
    assert transactions[0]["sender"] == "user4"
    assert transactions[0]["receiver"] == "user5"
    assert transactions[0]["amount"] == 50

    response = client.get(
        "/wallet/transactions", headers=_make_headers("user5", "bigsecret")
    )
    assert response.status_code == 200
    transactions = response.json["transactions"]
    assert len(transactions) == 1
    assert transactions[0]["sender"] == "user4"
    assert transactions[0]["receiver"] == "user5"
    assert transactions[0]["amount"] == 50


def test_transactions_with_transactions(client):
    response = client.get(
        "/wallet/transactions", headers=_make_headers("user1", "secret")
    )

    assert response.status_code == 200

    transactions = response.json["transactions"]
    assert len(transactions) == 1
    assert transactions[0]["sender"] == "user1"
    assert transactions[0]["receiver"] == "user2"
    assert transactions[0]["amount"] == 500

    response = client.get(
        "/wallet/transactions", headers=_make_headers("user2", "realsecret")
    )
    assert response.status_code == 200

    transactions = response.json["transactions"]
    assert len(transactions) == 1
    assert transactions[0]["sender"] == "user1"
    assert transactions[0]["receiver"] == "user2"
    assert transactions[0]["amount"] == 500


def test_transactions_no_transactions_yet(client):
    response = client.get(
        "/wallet/transactions", headers=_make_headers("user3", "supersecret")
    )
    assert response.status_code == 200
    transactions = response.json["transactions"]
    assert len(transactions) == 0
