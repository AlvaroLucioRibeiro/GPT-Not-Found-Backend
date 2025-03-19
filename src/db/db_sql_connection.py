import psycopg2
import os
from dotenv import load_dotenv

# load variables from .env file
load_dotenv()

# Variables to connect to the database
SUPABASE_USER = os.getenv("SUPABASE_USER", "test_user")
SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD", "test_password")
SUPABASE_HOST = os.getenv("SUPABASE_HOST", "localhost")
SUPABASE_PORT = os.getenv("SUPABASE_PORT", "5432")
SUPABASE_DATABASE = os.getenv("SUPABASE_DATABASE", "test_db")


def connect():
    """
    Establishes a connection to the PostgreSQL database.

    Returns:
        connection (psycopg2.extensions.connection): Database connection object.

    Raises:
        Exception: If an error occurs while connecting to the database.

    Example:
        >>> conn = connect()
        Connection established successfully.
    """
    try:
        connection = psycopg2.connect(
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD,
            host=SUPABASE_HOST,
            port=SUPABASE_PORT,
            database=SUPABASE_DATABASE,
        )
        print("Connection established successfully.")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")
        raise
