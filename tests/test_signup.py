"""Tests for signing up to activities (POST).

Arrange-Act-Assert structure in each test.
"""
from urllib.parse import quote


def test_successful_signup(client):
    # Arrange
    email = "test.user+signup@example.com"
    activity = "Chess Club"
    activity_q = quote(activity, safe="")
    email_q = quote(email, safe="")

    # Ensure not already present
    assert email not in client.get(f"/activities").json()[activity]["participants"]

    # Act
    res = client.post(f"/activities/{activity_q}/signup?email={email_q}")

    # Assert
    assert res.status_code == 200
    assert email in client.get(f"/activities").json()[activity]["participants"]


def test_duplicate_signup_returns_400(client):
    # Arrange
    email = "dup.user+signup@example.com"
    activity = "Chess Club"
    activity_q = quote(activity, safe="")
    email_q = quote(email, safe="")

    # Act: first signup
    first = client.post(f"/activities/{activity_q}/signup?email={email_q}")
    # Assert first succeeded
    assert first.status_code == 200

    # Act: duplicate signup
    second = client.post(f"/activities/{activity_q}/signup?email={email_q}")

    # Assert
    assert second.status_code == 400


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    email = "someone@example.com"
    activity_q = quote("NonExistentActivity", safe="")

    # Act
    res = client.post(f"/activities/{activity_q}/signup?email={quote(email, safe='')}")

    # Assert
    assert res.status_code == 404
