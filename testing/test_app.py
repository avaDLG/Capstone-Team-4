import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_class_filter(client):
    
    response = client.get("/filter-enrollment/CSCI1620")
    
    assert response.status_code == 200

    assert b'{"Fall":{"2021":139,"2022":213,"2023":217,"2024":242},"Spring":{"2022":145,"2023":172,"2024":167}}\n' in response.data
