def test_deployment_log_and_task_lifecycle(client):
    """End-to-end integration test: Task creation -> Status change -> Deployment logging."""
    # 1. Create DevOps Task
    task_res = client.post("/api/v1/tasks", json={
        "title": "Release v1.0.0 to Production",
        "description": "Trigger GitHub Actions CD workflow to deploy on AWS EC2",
        "priority": "critical"
    })
    assert task_res.status_code == 201
    task_id = task_res.json()["id"]

    # 2. Record Deployment Event
    deploy_res = client.post("/api/v1/deployments", json={
        "environment": "production",
        "version": "1.0.0",
        "commit_sha": "a1b2c3d4e5f6",
        "status": "success",
        "deployed_by": "GitHub Actions Autonomous CD",
        "summary": "FastAPI service container successfully booted on AWS EC2."
    })
    assert deploy_res.status_code == 201
    deploy_log = deploy_res.json()
    assert deploy_log["version"] == "1.0.0"
    assert deploy_log["status"] == "success"

    # 3. Complete DevOps Task
    update_res = client.put(f"/api/v1/tasks/{task_id}", json={"status": "completed"})
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "completed"

    # 4. Fetch Deployments Feed
    logs_res = client.get("/api/v1/deployments?limit=5")
    assert logs_res.status_code == 200
    logs = logs_res.json()
    assert len(logs) >= 1
    assert any(log["commit_sha"] == "a1b2c3d4e5f6" for log in logs)
