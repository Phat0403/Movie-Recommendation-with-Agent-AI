import pytest
from unittest.mock import MagicMock, AsyncMock
from services.auth import AuthService
from models.user import User

@pytest.fixture
def auth_service():
    user_controller = MagicMock()
    return AuthService(user_controller)

@pytest.mark.asyncio
async def test_send_register_otp_email_success(monkeypatch, auth_service):
    redis_client = AsyncMock()
    auth_service.user_controller.check_user_exists.return_value = False

    monkeypatch.setattr("core.auth.send_email_verification", lambda email: {"status": 200, "code": "123456"})
    monkeypatch.setattr("core.auth.password_validation", lambda pw: True)
    monkeypatch.setattr("core.auth.email_validation", lambda email: True)

    result = await auth_service.send_register_otp_email("john", "pass1234", "john@email.com", redis_client)
    assert result["status"] == 200
    assert "Registration initialized successfully" in result["message"]

@pytest.mark.asyncio
async def test_register_success(monkeypatch, auth_service):
    redis_client = AsyncMock()
    redis_client.get.side_effect = ["123456", "hashedpassword", "user@email.com"]
    redis_client.delete = AsyncMock()
    auth_service.user_controller.create = MagicMock()

    result = await auth_service.register("123456", username="john", redis_client=redis_client)
    assert result["status"] == 201
    assert result["message"] == "User registered successfully"

@pytest.mark.asyncio
async def test_resend_registration_otp(monkeypatch, auth_service):
    redis_client = AsyncMock()
    redis_client.get.side_effect = ["john@email.com", "pass1234"]

    monkeypatch.setattr("core.auth.send_email_verification", lambda email: {"status": 200, "code": "789654"})

    result = await auth_service.resend_registration_otp("john", redis_client)
    assert result["status"] == 200
    assert "Registration OTP resent successfully" in result["message"]

def test_login_success(monkeypatch):
    from services import auth  # giả sử auth.py nằm trong services/
    mock_user = User(username="john", password="bcrypt_hashed_pass", email="john@email.com", is_admin=False)

    user_controller = MagicMock()
    user_controller.check_user_exists.return_value = True
    user_controller.get.return_value = mock_user
    service = auth.AuthService(user_controller)

    monkeypatch.setattr("services.auth.verify_password", lambda pw, hashed: True)
    monkeypatch.setattr("services.auth.create_access_token", lambda data: "mocked_token")

    result = service.login("john", "password")
    assert result["status"] == 200
    assert result["access_token"] == "mocked_token"
    
def test_change_password_success(monkeypatch):
    from services import auth
    mock_user = User(username="john", password="bcrypt_old", email="john@email.com")

    user_controller = MagicMock()
    user_controller.check_user_exists.return_value = mock_user
    user_controller.get.return_value = mock_user
    user_controller.update.return_value = mock_user
    service = auth.AuthService(user_controller)

    monkeypatch.setattr("services.auth.verify_password", lambda a, b: True)
    monkeypatch.setattr("services.auth.password_validation", lambda pw: True)
    monkeypatch.setattr("services.auth.get_password_hash", lambda pw: "hashed_new")

    result = service.change_password("john", "old_pass", "new_pass123")
    assert result["status"] == 200


@pytest.mark.asyncio
async def test_send_password_reset_email(monkeypatch, auth_service):
    redis_client = AsyncMock()
    user = User(username="john", email="john@email.com")
    auth_service.user_controller.check_user_exists.return_value = True
    auth_service.user_controller.get.return_value = user

    monkeypatch.setattr("core.auth.send_email_verification", lambda email: {"status": 200, "code": "111222"})

    result = await auth_service.send_password_reset_email(redis_client, "john")
    assert result["status"] == 200
    assert result["message"] == "Password reset email sent successfully"

@pytest.mark.asyncio
async def test_verify_password_reset_code_success(auth_service):
    redis_client = AsyncMock()
    redis_client.get.return_value = "123456"

    result = await auth_service.verify_password_reset_code(redis_client, "john", "123456")
    assert result["status"] == 200
    assert result["message"] == "Code verified successfully"

def test_reset_password_success(monkeypatch, auth_service):
    mock_user = User(username="john", password="bcrypt_pass", email="john@email.com")
    auth_service.user_controller.check_user_exists.return_value = mock_user
    auth_service.user_controller.get.return_value = mock_user
    auth_service.user_controller.update.return_value = mock_user

    monkeypatch.setattr("core.auth.password_validation", lambda pw: True)
    monkeypatch.setattr("core.auth.get_password_hash", lambda pw: "new_hashed_pass")

    result = auth_service.reset_password("john", "new_pass_123")
    assert result["status"] == 200
    assert result["message"] == "Password reset successfully"
