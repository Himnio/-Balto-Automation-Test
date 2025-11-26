import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from paint_calculator.run import app as flask_app

@pytest.fixture
def app():
    """Create and configure a test instance of the Flask app."""
    flask_app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False  # Disable CSRF for testing
    })
    yield flask_app

@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def runner(app):
    """Create a test CLI runner for the Flask app."""
    return app.test_cli_runner()
    