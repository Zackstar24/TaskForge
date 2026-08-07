from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend import models
from backend.security import verify_password


def test_register_user(
    client: TestClient,
    db_session: Session,
) -> None:
    password = "secure-password"

    response = client.post(
        "/auth/register",
        json={
            "email": "User@Example.COM",
            "password": password,
        },
    )

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["email"] == "user@example.com"
    assert response_data["id"] >= 1
    assert "created_at" in response_data

    assert set(response_data) == {
        "id",
        "email",
        "created_at",
    }

    statement = select(models.User).where(
        models.User.email == "user@example.com",
    )
    db_user = db_session.scalar(statement)

    assert db_user is not None
    assert db_user.hashed_password != password
    assert verify_password(
        password,
        db_user.hashed_password,
    )


def test_register_user_rejects_invalid_email(
    client: TestClient,
) -> None:
    response = client.post(
        "/auth/register",
        json={
            "email": "not-an-email",
            "password": "secure-password",
        },
    )

    assert response.status_code == 422


def test_register_user_rejects_short_password(
    client: TestClient,
) -> None:
    response = client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "short",
        },
    )

    assert response.status_code == 422


def test_register_user_rejects_duplicate_email(
    client: TestClient,
) -> None:
    first_response = client.post(
        "/auth/register",
        json={
            "email": "User@Example.com",
            "password": "secure-password",
        },
    )

    second_response = client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "another-password",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "Email already registered",
    }

def test_login_user_returns_access_token(
    client: TestClient,
) -> None:
    client.post(
        "/auth/register",
        json={
            "email": "User@Example.com",
            "password": "secure-password",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "USER@example.com",
            "password": "secure-password",
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["token_type"] == "bearer"
    assert isinstance(response_data["access_token"], str)
    assert response_data["access_token"]


def test_login_user_rejects_incorrect_password(
    client: TestClient,
) -> None:
    client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "secure-password",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Incorrect email or password",
    }
    assert response.headers["www-authenticate"] == "Bearer"


def test_login_user_rejects_unknown_email(
    client: TestClient,
) -> None:
    response = client.post(
        "/auth/login",
        json={
            "email": "missing@example.com",
            "password": "secure-password",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Incorrect email or password",
    }


def test_read_current_user(
    client: TestClient,
) -> None:
    register_response = client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "secure-password",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "secure-password",
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["email"] == "user@example.com"
    assert response_data["id"] >= 1
    assert "created_at" in response_data

    assert set(response_data) == {
        "id",
        "email",
        "created_at",
    }


def test_read_current_user_requires_token(
    client: TestClient,
) -> None:
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Could not validate credentials",
    }
    assert response.headers["www-authenticate"] == "Bearer"


def test_read_current_user_rejects_invalid_token(
    client: TestClient,
) -> None:
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Could not validate credentials",
    }


def test_login_user_rejects_invalid_email(
    client: TestClient,
) -> None:
    response = client.post(
        "/auth/login",
        json={
            "email": "not-an-email",
            "password": "secure-password",
        },
    )

    assert response.status_code == 422