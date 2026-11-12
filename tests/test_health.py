def test_ping_endpoint(client):
    """Verify lightweight ping health endpoint."""
    response = client.get("/api/v1/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["ping"] == "pong"
    assert "timestamp" in data


def test_health_endpoint(client):
    """Verify detailed service health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "app_name" in data
    assert "version" in data
    assert "database_connected" in data
