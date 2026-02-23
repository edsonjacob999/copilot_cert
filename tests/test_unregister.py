"""Tests for unregistering participants (DELETE).

Uses Arrange-Act-Assert pattern.
"""
from urllib.parse import quote


def test_unregister_success(client):
    # Arrange
    email = "to.remove+test@example.com"
    activity = "Programming Class"
    activity_q = quote(activity, safe="")
    email_q = quote(email, safe="")

    # Ensure participant exists by signing up
    signup = client.post(f"/activities/{activity_q}/signup?email={email_q}")
    assert signup.status_code == 200

    # Act
    res = client.delete(f"/activities/{activity_q}/signup?email={email_q}")

    # Assert
    assert res.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_non_member_returns_404(client):
    # Arrange
    email = "not.in.list@example.com"
    activity_q = quote("Programming Class", safe="")

    # Act
    res = client.delete(f"/activities/{activity_q}/signup?email={quote(email, safe='')}")

    # Assert
    assert res.status_code == 404


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    email = "someone@example.com"
    activity_q = quote("NoSuchActivity", safe="")

    # Act
    res = client.delete(f"/activities/{activity_q}/signup?email={quote(email, safe='')}")

    # Assert
    assert res.status_code == 404
