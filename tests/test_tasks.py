from typing import Any

import pytest
from fastapi.testclient import TestClient

from backend.main import get_allowed_origins

@pytest.fixture(autouse=True)
def authenticate_task_client(
    client: TestClient,
) -> None:
    email = "task-owner@example.com"
    password = "secure-password"

    register_response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    client.headers.update(
        {
            "Authorization": f"Bearer {access_token}",
        }
    )


def create_auth_headers(
    client: TestClient,
    email: str,
) -> dict[str, str]:
    password = "secure-password"

    register_response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {access_token}",
    }


def create_test_task(
    client: TestClient,
    title: str = "Test task",
    description: str | None = "Task created during testing",
    priority: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "title": title,
        "description": description,
    }

    if priority is not None:
        payload["priority"] = priority

    response = client.post(
        "/tasks",
        json=payload,
    )

    assert response.status_code == 201

    return response.json()


def test_home_endpoint(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "TaskForge backend is running!"
    }

def test_cors_allows_frontend_origin(
    client: TestClient,
) -> None:
    response = client.options(
        "/tasks",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert (
        response.headers["access-control-allow-origin"]
        == "http://localhost:5173"
    )

def test_allowed_origins_includes_configured_frontend(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "FRONTEND_ORIGIN",
        "https://taskforge-zack.onrender.com/",
    )

    origins = get_allowed_origins()

    assert "https://taskforge-zack.onrender.com" in origins

def test_create_task(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Write automated tests",
            "description": "Test the TaskForge API",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Write automated tests"
    assert data["description"] == "Test the TaskForge API"
    assert data["priority"] == "medium"
    assert data["completed"] is False
    assert data["created_at"] is not None


def test_create_task_rejects_blank_title(
    client: TestClient,
) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "   ",
            "description": "This request should fail",
        },
    )

    assert response.status_code == 422


def test_create_task_with_priority(
    client: TestClient,
) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "High-priority task",
            "description": "This task is urgent",
            "priority": "high",
        },
    )

    assert response.status_code == 201
    assert response.json()["priority"] == "high"


def test_create_task_rejects_invalid_priority(
    client: TestClient,
) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Invalid priority task",
            "priority": "urgent",
        },
    )

    assert response.status_code == 422


def test_read_tasks(client: TestClient) -> None:
    first_task = create_test_task(
        client,
        title="First task",
    )
    second_task = create_test_task(
        client,
        title="Second task",
    )

    response = client.get("/tasks")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert [task["id"] for task in data] == [
        first_task["id"],
        second_task["id"],
    ]
    assert [task["title"] for task in data] == [
        "First task",
        "Second task",
    ]
    assert [task["priority"] for task in data] == [
        "medium",
        "medium",
    ]


def test_read_single_task(client: TestClient) -> None:
    created_task = create_test_task(
        client,
        title="Retrieve this task",
    )

    response = client.get(
        f"/tasks/{created_task['id']}"
    )

    assert response.status_code == 200
    assert response.json() == created_task


def test_read_missing_task_returns_404(
    client: TestClient,
) -> None:
    response = client.get("/tasks/9999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }


def test_update_task(client: TestClient) -> None:
    created_task = create_test_task(
        client,
        title="Incomplete task",
        description="This description should remain unchanged",
    )

    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={
            "title": "Updated task",
            "completed": True,
        },
    )

    assert response.status_code == 200

    updated_task = response.json()

    assert updated_task["id"] == created_task["id"]
    assert updated_task["title"] == "Updated task"
    assert (
        updated_task["description"]
        == "This description should remain unchanged"
    )
    assert updated_task["priority"] == "medium"
    assert updated_task["completed"] is True
    assert updated_task["created_at"] == created_task["created_at"]

    saved_response = client.get(
        f"/tasks/{created_task['id']}"
    )

    assert saved_response.status_code == 200
    assert saved_response.json() == updated_task


def test_update_task_priority(
    client: TestClient,
) -> None:
    created_task = create_test_task(
        client,
        title="Change this priority",
        priority="low",
    )

    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={
            "priority": "high",
        },
    )

    assert response.status_code == 200

    updated_task = response.json()

    assert updated_task["priority"] == "high"
    assert updated_task["title"] == created_task["title"]
    assert updated_task["completed"] == created_task["completed"]

    saved_response = client.get(
        f"/tasks/{created_task['id']}"
    )

    assert saved_response.status_code == 200
    assert saved_response.json()["priority"] == "high"


def test_update_task_rejects_null_priority(
    client: TestClient,
) -> None:
    created_task = create_test_task(client)

    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={
            "priority": None,
        },
    )

    assert response.status_code == 422


def test_update_task_rejects_empty_body(
    client: TestClient,
) -> None:
    created_task = create_test_task(client)

    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={},
    )

    assert response.status_code == 422


def test_update_missing_task_returns_404(
    client: TestClient,
) -> None:
    response = client.patch(
        "/tasks/9999",
        json={
            "completed": True,
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }


def test_delete_task(client: TestClient) -> None:
    created_task = create_test_task(
        client,
        title="Delete this task",
    )

    delete_response = client.delete(
        f"/tasks/{created_task['id']}"
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(
        f"/tasks/{created_task['id']}"
    )

    assert get_response.status_code == 404

    list_response = client.get("/tasks")

    assert list_response.status_code == 200
    assert list_response.json() == []


def test_delete_missing_task_returns_404(
    client: TestClient,
) -> None:
    response = client.delete("/tasks/9999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }


def test_invalid_task_id_returns_422(
    client: TestClient,
) -> None:
    response = client.get("/tasks/0")

    assert response.status_code == 422

def test_task_routes_require_authentication(
    client: TestClient,
) -> None:
    client.headers.pop("Authorization", None)

    response = client.get("/tasks")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Could not validate credentials",
    }

def test_users_only_see_their_own_tasks(
    client: TestClient,
) -> None:
    first_user_task = create_test_task(
        client,
        title="First user's task",
    )

    second_user_headers = create_auth_headers(
        client,
        "second-user@example.com",
    )

    second_task_response = client.post(
        "/tasks",
        headers=second_user_headers,
        json={
            "title": "Second user's task",
        },
    )

    assert second_task_response.status_code == 201

    first_user_response = client.get("/tasks")

    assert first_user_response.status_code == 200
    assert first_user_response.json() == [
        first_user_task,
    ]

    second_user_response = client.get(
        "/tasks",
        headers=second_user_headers,
    )

    assert second_user_response.status_code == 200

    second_user_tasks = second_user_response.json()

    assert len(second_user_tasks) == 1
    assert (
        second_user_tasks[0]["title"]
        == "Second user's task"
    )


def test_user_cannot_access_another_users_task(
    client: TestClient,
) -> None:
    first_user_task = create_test_task(
        client,
        title="Private task",
    )

    second_user_headers = create_auth_headers(
        client,
        "second-user@example.com",
    )

    task_url = f"/tasks/{first_user_task['id']}"

    get_response = client.get(
        task_url,
        headers=second_user_headers,
    )

    patch_response = client.patch(
        task_url,
        headers=second_user_headers,
        json={
            "title": "Unauthorized change",
        },
    )

    delete_response = client.delete(
        task_url,
        headers=second_user_headers,
    )

    assert get_response.status_code == 404
    assert patch_response.status_code == 404
    assert delete_response.status_code == 404

    owner_response = client.get(task_url)

    assert owner_response.status_code == 200
    assert (
        owner_response.json()["title"]
        == "Private task"
    )