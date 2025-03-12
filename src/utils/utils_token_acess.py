import os
import jwt
from typing import Optional
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone


# load variables from .env
load_dotenv()

# configuration to generate token
SECRET_KEY = os.getenv("SECRET_KEY")  
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))  


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
