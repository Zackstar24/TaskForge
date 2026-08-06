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