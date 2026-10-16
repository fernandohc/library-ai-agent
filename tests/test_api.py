import pytest
from fastapi.testclient import TestClient

import src.api as api


class FakeLibraryAssistant:
    """Simulates the assistant without calling external services."""

    def ask(self, question: str) -> dict:
        return {
            "agent": "book_search",
            "answer": f"Simulated answer for: {question}",
        }


@pytest.fixture
def client(monkeypatch):
    # Replace the real assistant before the application starts.
    monkeypatch.setattr(
        api,
        "LibraryAssistant",
        FakeLibraryAssistant,
    )

    with TestClient(api.app) as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "application": "library-ai-agent",
    }


def test_ask_with_valid_question(client):
    response = client.post(
        "/ask",
        json={"question": "Find horror books."},
    )

    assert response.status_code == 200
    assert response.json() == {
        "agent": "book_search",
        "answer": "Simulated answer for: Find horror books.",
    }


def test_ask_without_question(client):
    response = client.post("/ask", json={})

    assert response.status_code == 422


def test_ask_with_empty_question(client):
    response = client.post(
        "/ask",
        json={"question": ""},
    )

    assert response.status_code == 422


def test_ask_with_question_too_long(client):
    response = client.post(
        "/ask",
        json={"question": "a" * 2001},
    )

    assert response.status_code == 422
