import requests
import os
import jwt
import asyncio
from faker import Faker
from typing import Dict, Optional
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from src.tests.utils.utils import (
    generate_random_email,
    generate_password,
    generate_cell_phone_number,
    generate_cpf,
    generate_cnpj,
)
from db.CRUD.read import get_customer_by_email

fake = Faker()

# Load environment variables
load_dotenv()

# Definitions for test data
CUSTOMER_TEST_API = {
    "full_name": fake.name(),
    "email": generate_random_email(),
    "phone": generate_cell_phone_number(),  # Adding required field
    "address": fake.address(),  # Adding required field
    "cpf_cnpj": fake.random_element(
        elements=[generate_cpf(), generate_cnpj()]
    ),  # Adding required field
    "password_hash": generate_password(),
    "role": fake.random_element(elements=["customer", "admin"]),
}

URL = "https://gpt-not-found.vercel.app"
LOGIN_ROUTE = "/auth/login"
REGISTER_ROUTE = "/auth/register"
TOKEN = None

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

# Authentication scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def test_register_customer():
    """
    Tests user registration via API.

    Sends a POST request to register a new user and asserts
    that the response contains a success message.
    """
    response = requests.post(URL + REGISTER_ROUTE, json=CUSTOMER_TEST_API)
    json_response = response.json()

    assert response is not None
    assert "message" in json_response
    assert json_response["message"].startswith("User")
    assert json_response["message"].endswith("registered successfully!")


def test_login_customer():
    """
    Tests user login and token retrieval.

    Sends a POST request to log in with the registered user credentials.
    Asserts that a valid access token is returned.
    """
    login_response = requests.post(
        URL + LOGIN_ROUTE,
        data={
            "username": CUSTOMER_TEST_API["email"],
            "password": CUSTOMER_TEST_API["password_hash"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert login_response.status_code == 200, f"Login error: {login_response.json()}"

    json_response = login_response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"

    global TOKEN
    TOKEN = json_response["access_token"]


def test_invalid_login():
    """
    Tests login attempt with invalid credentials.

    Sends a POST request with incorrect login credentials
    and asserts that the API returns an authentication error.
    """
    invalid_response = requests.post(
        URL + LOGIN_ROUTE,
        data={
            "username": CUSTOMER_TEST_API["email"],
            "password": "invalid_password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert invalid_response.status_code == 400
    assert invalid_response.json()["detail"] == "Invalid email or password"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Generates a JWT token.

    Args:
        data (dict): The payload data to encode in the token.
        expires_delta (timedelta, optional): The expiration time of the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def test_create_access_token():
    """
    Tests JWT token creation.

    Ensures that the generated token is a valid string.
    """
    data = {"sub": CUSTOMER_TEST_API["email"]}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """
    Decodes the JWT and retrieves the authenticated user data.

    Args:
        token (str): The JWT token provided in the request.

    Returns:
        Dict: The authenticated user's data.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Fetch the user from the database using the extracted email
        user = await get_customer_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def test_get_current_user():
    """
    Tests retrieving the current authenticated user asynchronously.

    Generates a valid token and ensures the function correctly
    retrieves user details without errors.
    """
    token = create_access_token({"sub": CUSTOMER_TEST_API["email"]})
    user = asyncio.run(get_current_user(token))
    assert user is not None
