import pytest
from fastapi.testclient import TestClient
from filespy.api import app

client = TestClient(app)


# ============================================
# FIXTURES
# ============================================

@pytest.fixture
def sample_file(tmp_path):
    """Create a temporary test file."""
    file = tmp_path / "test.txt"
    file.write_text("Hello world\nThis is line two\nAnd line three")
    return str(file)


# ============================================
# HEALTH ENDPOINT TESTS
# ============================================

def test_health_endpoint():
    """Test that health endpoint returns ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ============================================
# ANALYZE ENDPOINT TESTS
# ============================================

def test_analyze_valid_file(sample_file):
    """Test analyzing a real file returns correct stats."""
    response = client.post(
        "/analyze",
        json={"filepath": sample_file}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["lines"] == 3
    assert data["words"] == 9
    assert data["extension"] == ".txt"
    assert data["size_kb"] > 0
    assert "analyzed_at" in data


def test_analyze_missing_file():
    """Test that missing file returns 404."""
    response = client.post(
        "/analyze",
        json={"filepath": "fakefile.txt"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "File not found"}


def test_analyze_missing_filepath_field():
    """Test that missing filepath field returns 422."""
    response = client.post(
        "/analyze",
        json={}
    )
    assert response.status_code == 422


# ============================================
# HISTORY ENDPOINT TESTS
# ============================================

def test_history_starts_empty():
    """Test that history is empty at start."""
    client.delete("/history")
    response = client.get("/history")
    assert response.status_code == 200
    assert response.json()["total"] == 0
    assert response.json()["history"] == []


def test_history_records_analysis(sample_file):
    """Test that history records each analysis."""
    client.delete("/history")
    client.post("/analyze", json={"filepath": sample_file})
    response = client.get("/history")
    assert response.json()["total"] == 1


def test_delete_history(sample_file):
    """Test that delete clears all history."""
    client.post("/analyze", json={"filepath": sample_file})
    client.delete("/history")
    response = client.get("/history")
    assert response.json()["total"] == 0