import pytest
from fastapi import HTTPException
from src.utils.utils_validation import (
    get_password_hash,
    verify_password,
    validate_password_strength,
    validate_email_format,
)


def test_get_password_hash():
    """
    Tests if the password hashing function correctly hashes a password.
    """
    password = "StrongPass123!"
    hashed_password = get_password_hash(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != password


def test_verify_password():
    """
    Tests if the password verification function correctly matches a password to its hash.
    """
    password = "StrongPass123!"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) is True
    assert verify_password("WrongPass", hashed_password) is False


def test_validate_password_strength():
    """
    Tests if weak passwords raise an HTTPException and strong passwords pass validation.
    """
    with pytest.raises(HTTPException) as excinfo:
        validate_password_strength("12345")
    assert excinfo.value.status_code == 400
    assert "The password must be at least 6 characters long." in str(
        excinfo.value.detail
    )

    # Should not raise an exception
    validate_password_strength("StrongPass")


def test_validate_email_format():
    """
    Tests if valid emails pass validation and invalid emails raise an HTTPException.
    """
    valid_emails = [
        "test@example.com",
        "user.name@domain.br",
        "valid-email@valid.com",
    ]

    for email in valid_emails:
        validate_email_format(email)

    invalid_emails = [
        "invalid-email",
        "user@domain",
        "@missinguser.com",
        "user@domain.org",
        "name@domain.xyz",
    ]

    for email in invalid_emails:
        with pytest.raises(HTTPException) as excinfo:
            validate_email_format(email)
        assert excinfo.value.status_code == 400
        assert (
            "The email must be in the format 'name@domain.com' or 'name@domain.br'."
            in str(excinfo.value.detail)
        )
