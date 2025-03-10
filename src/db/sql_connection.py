import psycopg2
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Variáveis de ambiente para conexão com o banco de dados
SUPABASE_USER = os.getenv("SUPABASE_USER")
SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD")
SUPABASE_HOST = os.getenv("SUPABASE_HOST")
SUPABASE_PORT = os.getenv("SUPABASE_PORT")
SUPABASE_DATABASE = os.getenv("SUPABASE_DATABASE")


def connect():
    """
    Estabelece uma conexão com o banco de dados PostgreSQL.

    Returns:
        connection (psycopg2.extensions.connection): Objeto de conexão com o banco de dados.

    Raises:
        Exception: Se ocorrer um erro ao conectar ao banco de dados.

    Exemplo:
        >>> conn = connect()
        Conexão estabelecida com sucesso.
    """
    try:
        connection = psycopg2.connect(
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD,
            host=SUPABASE_HOST,
            port=SUPABASE_PORT,
            database=SUPABASE_DATABASE,
        )
        print("Conexão estabelecida com sucesso.")
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise
