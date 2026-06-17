from pathlib import Path

from app import create_app
from app.config import Config
from app.extensions import db


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = str(Path("/tmp/securevault-test-sessions"))


def test_register_login_and_dashboard_flow():
    app = create_app(TestConfig)
    client = app.test_client()

    register_response = client.post(
        "/auth/register",
        data={
            "username": "student",
            "password": "VeryStrongPass123!",
            "confirm_password": "VeryStrongPass123!",
        },
        follow_redirects=True,
    )
    assert b"Account created" in register_response.data

    login_response = client.post(
        "/auth/login",
        data={"username": "student", "password": "VeryStrongPass123!"},
        follow_redirects=True,
    )
    assert b"Vault unlocked" in login_response.data

    add_response = client.post(
        "/vault/credentials/new",
        data={
            "service": "Example Mail",
            "login_name": "student@example.com",
            "password": "GeneratedPassword123!",
            "url": "https://example.com",
            "notes": "demo note",
        },
        follow_redirects=True,
    )
    assert b"Credential saved securely" in add_response.data
    assert b"Example Mail" in add_response.data

    with app.app_context():
        db.session.remove()
