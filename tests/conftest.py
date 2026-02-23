from fastapi.testclient import TestClient
import copy
import pytest
import urllib.parse

import src.app as app_module


@pytest.fixture
def client():
    """Provide a TestClient and ensure `src.app.activities` is restored after each test.

    This keeps tests isolated (Arrange/Act/Assert pattern used in test files).
    """
    # Arrange: snapshot the activities
    original = copy.deepcopy(app_module.activities)

    client = TestClient(app_module.app)

    yield client

    # Teardown: restore original activities
    app_module.activities.clear()
    app_module.activities.update(original)
