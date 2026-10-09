from typing import cast
from unittest.mock import patch

import pytest
import requests
from pydantic import ValidationError

from Scripts.api_client import User, get_user


@patch("Scripts.api_client.requests.get")
def test_get_user(mock_get):
    mock_get.return_value.json.return_value = {
        "id": 1,
        "name": "John Doe",
        "username": "john_doe",
        "email": "john.doe@example.com"
    }

    user = get_user(1)
    mock_get.assert_called_once_with(
    "https://jsonplaceholder.typicode.com/users/1",
    timeout=10,
)
    assert user.id == 1
    assert user.name == "John Doe"

@patch("Scripts.api_client.requests.get")
def test_get_user_invalid_mock(mock_get):
    mock_get.return_value.json.return_value = {
        "id": "abc",
        "name": "John Doe",
        "username": "john_doe",
        "email": "john.doe@example.com"
    }
    with pytest.raises(ValidationError) as exc_info:
        get_user(1)
    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("id",)
    assert errors[0]["input"] == "abc"    

@patch("Scripts.api_client.requests.get")
def test_incomplete_user_data(mock_get):
    mock_get.return_value.json.return_value = {
        "id": 1,
        "name": "John Doe",
        "username": "john_doe"
    }
    with pytest.raises(ValidationError) as exc_info:
        get_user(1)
    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("email",)

@patch("Scripts.api_client.requests.get")
def test_multiple_errors(mock_get):
    mock_get.return_value.json.return_value = {
        "id": "abc",
        "name": "John Doe",
        "username": "john_doe"
    }
    with pytest.raises(ValidationError) as exc_info:
        get_user(1)
    errors = exc_info.value.errors()
    error_fields = [error["loc"] for error in errors]
    assert ("id",) in error_fields
    assert ("email",) in error_fields

@patch("Scripts.api_client.requests.get")
def test_get_user_not_found(mock_get):
    mock_get.return_value.raise_for_status.side_effect = requests.HTTPError(
        "404 Client Error"
    )

    with pytest.raises(requests.HTTPError):
        get_user(1)
