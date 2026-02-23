"""Tests for root redirection and activities listing.

Uses Arrange-Act-Assert pattern.
"""
from urllib.parse import urlparse


def test_root_redirect(client):
    # Arrange: client fixture

    # Act
    res = client.get("/")

    # Assert
    # TestClient follows redirects by default; accept either a redirect
    # response or the final 200 HTML content.
    if res.status_code in (301, 302, 307, 308):
        loc = res.headers.get("location", "")
        assert "/static/index.html" in loc
    else:
        # Followed redirect -- ensure the returned page looks like the index
        assert res.status_code == 200
        assert "Mergington High School" in res.text


def test_get_activities(client):
    # Arrange

    # Act
    res = client.get("/activities")

    # Assert
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # Known activity keys should exist
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
