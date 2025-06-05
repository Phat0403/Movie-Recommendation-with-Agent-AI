import pytest
from core import auth
from jose import jwt
from unittest.mock import patch, MagicMock

# Mock settings
class MockSettings:
    SECRET_KEY = "testsecret"
    ALGORITHM = "HS256"
    GMAIL = "test@gmail.com"
    GMAIL_PASSWORD = "password123"

@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    monkeypatch.setattr("core.auth.settings", MockSettings())

# ----------------------------
# Password-related Tests
# ----------------------------

def test_verify_password():
    plain = "strongpassword"
    hashed = auth.get_password_hash(plain)
    assert auth.verify_password(plain, hashed) is True
    assert auth.verify_password("wrongpass", hashed) is False

def test_password_validation():
    assert auth.password_validation("12345678") is True
    assert auth.password_validation("abc") is False

# ----------------------------
# JWT Token Tests
# ----------------------------

def test_create_and_decode_access_token():
    data = {"username": "john", "role": "admin"}
    token = auth.create_access_token(data)
    decoded = auth.decode_token(token)
    assert decoded["username"] == "john"
    assert decoded["role"] == "admin"

def test_decode_token_invalid():
    invalid_token = "invalid.token.value"
    assert auth.decode_token(invalid_token) is None

def test_get_username_from_token():
    token = auth.create_access_token({"username": "alice"})
    assert auth.get_username_from_token(token) == "alice"

def test_get_role_from_token():
    token = auth.create_access_token({"role": "moderator"})
    assert auth.get_role_from_token(token) == "moderator"

# ----------------------------
# Email validation
# ----------------------------

def test_email_validation():
    assert auth.email_validation("user@example.com") is True
    assert auth.email_validation("bad-email@") is False

# ----------------------------
# Send Email Verification
# ----------------------------

@patch("core.auth.smtplib.SMTP")
def test_send_email_verification_success(mock_smtp):
    instance = mock_smtp.return_value.__enter__.return_value
    instance.send_message = MagicMock()

    result = auth.send_email_verification("user@example.com")
    assert result["status"] == 200
    assert result["email"] == "user@example.com"
    assert "code" in result

@patch("core.auth.smtplib.SMTP", side_effect=Exception("SMTP failed"))
def test_send_email_verification_failure(mock_smtp):
    result = auth.send_email_verification("user@example.com")
    assert result["status"] == 500
    assert result["error"] == "Failed to send email"
