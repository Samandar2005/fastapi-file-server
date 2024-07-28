import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "postgresql://samandar:1234@localhost/file_server_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

UPLOAD_FOLDER = "app/uploaded_files"
EXCEL_PATH = "app/file_records.xlsx"


@pytest.fixture(scope="module")
def setup_and_teardown():
    if os.path.exists(UPLOAD_FOLDER):
        for root, dirs, files in os.walk(UPLOAD_FOLDER, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    yield
    if os.path.exists(UPLOAD_FOLDER):
        for root, dirs, files in os.walk(UPLOAD_FOLDER, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    if os.path.exists(EXCEL_PATH):
        os.remove(EXCEL_PATH)


def test_upload_and_get_file(setup_and_teardown):
    file_name = "test.txt"
    file_content = b"Test file content"
    files = {"file": (file_name, file_content)}

    response = client.post("/upload/", files=files)
    assert response.status_code == 200
    json_response = response.json()
    assert "message" in json_response
    assert json_response["message"] == "File uploaded successfully"
    assert "url" in json_response

    file_url = json_response["url"]
    date_part = file_url.split('/')[1]
    filename_part = file_url.split('/')[2]

    response = client.get(f"/{date_part}/{filename_part}")
    assert response.status_code == 200
    assert response.content == file_content

    response = client.post("/upload/", files=files)
    assert response.status_code == 200
    json_response = response.json()
    assert "message" in json_response
    assert json_response["message"] == "File already exists"
    assert "url" in json_response
    assert json_response["url"] == file_url


if __name__ == "__main__":
    pytest.main()
