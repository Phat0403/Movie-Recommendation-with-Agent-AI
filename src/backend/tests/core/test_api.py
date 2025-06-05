import pytest
from fastapi import Request
from httpx import Response, Request as HTTPXRequest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from core.api import get_user_from_request

@pytest.mark.asyncio
async def test_missing_authorization_header():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {}
    
    result = await get_user_from_request(mock_request)
    assert result["status_code"] == 401
    assert result["message"] == "Authorization header is missing"

@pytest.mark.asyncio
async def test_invalid_authorization_format():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": "Token abc123"}
    
    result = await get_user_from_request(mock_request)
    assert result["status_code"] == 401
    assert result["message"] == "Invalid authorization header format"

@pytest.mark.asyncio
async def test_missing_token():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer "}
    
    result = await get_user_from_request(mock_request)
    assert result["status_code"] == 401
    assert result["message"] == "Token is required"

@pytest.mark.asyncio
@patch("core.api.httpx.AsyncClient.get")
async def test_failed_user_info_fetch(mock_get):
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer validtoken"}

    mock_response = Response(status_code=403, request=HTTPXRequest("GET", "http://localhost"))
    mock_get.return_value = mock_response
    
    result = await get_user_from_request(mock_request)
    assert result["status_code"] == 403
    assert result["message"] == "Failed to fetch user information"

@pytest.mark.asyncio
@patch("core.api.httpx.AsyncClient.get")
async def test_successful_user_info_fetch(mock_get):
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer validtoken"}

    mock_user_data = {"id": 1, "username": "john_doe"}
    mock_response = Response(
        status_code=200,
        request=HTTPXRequest("GET", "http://localhost"),
        json=mock_user_data
    )

    # Override .json method because Response.json() normally parses the body
    mock_response.json = lambda: mock_user_data
    mock_get.return_value = mock_response

    result = await get_user_from_request(mock_request)
    assert result["status_code"] == 200
    assert result["message"] == "User information retrieved successfully"
    assert result["user"] == mock_user_data

@pytest.mark.asyncio
@patch("core.api.httpx.AsyncClient.get", new_callable=AsyncMock)
async def test_request_error(mock_get):
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer sometoken"}
    mock_get.side_effect = httpx.RequestError("Connection failed", request=HTTPXRequest("GET", "http://localhost"))

    result = await get_user_from_request(mock_request)
    assert result["status_code"] == 500
    assert "Request error" in result["message"]
