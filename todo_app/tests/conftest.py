import pytest
import os,sys
sys.path.append('/srv/www/todo_app')
from app import app as flask_app

token = os.getenv('token')
key = os.getenv('key')

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_unittestWebServer(app, client):
        result = client.get('/')
        assert result.status_code == 200

