def test_create_and_get_task(client):
    """Test creating a DevOps task and retrieving it."""
    payload = {
        "title": "Configure Terraform State Backend",
        "description": "Set up S3 bucket and DynamoDB locking table.",
        "priority": "high"
    }
    response = client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert created["id"] is not None
    assert created["title"] == payload["title"]
    assert created["priority"] == "high"
    assert created["status"] == "pending"

    # Retrieve by ID
    get_res = client.get(f"/api/v1/tasks/{created['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == payload["title"]


def test_list_tasks(client):
    """Test listing tasks."""
    client.post("/api/v1/tasks", json={"title": "Task 1", "priority": "low"})
    client.post("/api/v1/tasks", json={"title": "Task 2", "priority": "medium"})

    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 2


def test_update_task_status(client):
    """Test updating task status and details."""
    created = client.post("/api/v1/tasks", json={"title": "Deploy to EC2", "priority": "critical"}).json()
    task_id = created["id"]

    update_payload = {
        "status": "completed",
        "priority": "high"
    }
    update_res = client.put(f"/api/v1/tasks/{task_id}", json=update_payload)
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["status"] == "completed"
    assert updated["priority"] == "high"


def test_delete_task(client):
    """Test deleting a task."""
    created = client.post("/api/v1/tasks", json={"title": "Temporary Task"}).json()
    task_id = created["id"]

    del_res = client.delete(f"/api/v1/tasks/{task_id}")
    assert del_res.status_code == 204

    # Verify 404 after deletion
    get_res = client.get(f"/api/v1/tasks/{task_id}")
    assert get_res.status_code == 404


def test_task_not_found(client):
    """Test retrieving non-existent task."""
    response = client.get("/api/v1/tasks/99999")
    assert response.status_code == 404
