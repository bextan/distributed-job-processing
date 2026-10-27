from unittest.mock import patch, MagicMock

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]


def test_submit_data_processing_job(client):
    payload = {
        "job_type": "data_processing",
        "payload": {"records": 50}
    }
    response = client.post("/api/v1/jobs", json=payload)
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "QUEUED"


def test_get_job_status_eager(client):
    payload = {
        "job_type": "notification",
        "payload": {"recipient": "test@example.com"}
    }
    submit_res = client.post("/api/v1/jobs", json=payload)
    assert submit_res.status_code == 202
    job_id = submit_res.json()["job_id"]

    mock_async_result = MagicMock()
    mock_async_result.status = "SUCCESS"
    mock_async_result.result = {"status": "SENT", "recipient": "test@example.com"}
    mock_async_result.failed.return_value = False

    with patch("app.api.v1.endpoints.jobs.AsyncResult", return_value=mock_async_result):
        status_res = client.get(f"/api/v1/jobs/{job_id}")
        assert status_res.status_code == 200
        status_data = status_res.json()
        assert status_data["job_id"] == job_id
        assert status_data["status"] == "SUCCESS"