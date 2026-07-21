from typing import Any

from fastapi.testclient import TestClient


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