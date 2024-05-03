import json
from fastapi.testclient import TestClient

from app.main import app
from app.models.ticket import TicketDataResponse

client = TestClient(app)


mock_ticket_data = [
    {"summary": "Test summary 1", "description": "Test description 1", "file_path": ""},
    {"summary": "Test summary 2", "description": "Test description 2", "file_path": ""}
]


mock_generate_response_data = {"id": "10016", "key": "SCRUM-14", "self": "https://jira.example.com"}


def mock_generate_request(**kwargs):
    return type('Response', (), {'status_code': 201, 'text': json.dumps(mock_generate_response_data)})


def test_generate_tickets_valid_token():
    app.create_jira_ticket = lambda ticket_data: mock_generate_response_data

    valid_token = "fakehashedsecret"

    response = client.post("/generate", json=mock_ticket_data, headers={"Authorization": f"Bearer {valid_token}"})

    assert response.status_code == 200

    assert isinstance(response.json(), list)
    assert len(response.json()) == len(mock_ticket_data)


def test_generate_tickets_no_token():
    app.create_jira_ticket = lambda ticket_data: mock_generate_response_data

    response = client.post("/generate", json=mock_ticket_data)

    assert response.status_code == 401
