from fastapi.testclient import TestClient

from app.main import app
from app.utils.dependencies import get_postgres_manager


client = TestClient(app)

def override_get_postgres_manager():
    postgres_manager = None
    try:
        yield postgres_manager
    finally:
        pass


app.dependency_overrides[get_postgres_manager] = override_get_postgres_manager

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == '"Waiting List Service"'


def test_errors():
    """
    mock the postgres db
    send requests that will trigger the errors handled
    make sure that the functions alter the db properly by checking afterward
    """
    pass
