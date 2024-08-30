from fastapi.testclient import TestClient
from app.main import app
import sys


client = TestClient(app)


def test_read_root_not_authenticated():
    response = client.get("/")
    assert response.status_code == 307  # Redirect
    assert response.headers["location"] == "/auth/login"


def test_auth_login():
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert "auth_url" in response.url


def test_auth_callback_invalid_state():
    response = client.get("/auth/callback?state=invalid_state")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid state parameter"}


def test_auth_logout():
    response = client.get("/auth/logout")
    assert response.status_code == 307  # Redirect
    assert response.headers["location"] == "/auth/login"


def test_list_files_not_authenticated():
    response = client.get("/drive/list-files")
    assert response.status_code == 403
    assert response.json() == {"detail": "User not authenticated"}


def test_upload_file_form():
    response = client.get("/drive/upload-file")
    assert response.status_code == 200
    assert "upload_file.html" in response.text


def test_upload_file_route_not_authenticated():
    response = client.post("/drive/upload-file", data={"file_path": None, "folder_id": None})
    assert response.status_code == 307
    assert response.headers["location"] == "/auth/login"


def test_download_file_route_not_authenticated():
    response = client.get("/drive/download-file/test_file_id")
    assert response.status_code == 307
    assert response.headers["location"] == "/auth/login"


def test_delete_file_route_not_authenticated():
    response = client.post("/drive/delete-file/test_file_id")
    assert response.status_code == 307
    assert response.headers["location"] == "/auth/login"
