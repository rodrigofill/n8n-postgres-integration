import os
from dotenv import load_dotenv

class ApplicationConfig:
    load_dotenv(override=True)
    BASE_PATH = os.environ.get("BASE_PATH", "/")
    ENV = os.environ.get("ENV", "local")
    VERSION = os.environ.get('VERSION', '1.0.0')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SQLALCHEMY_PREFIX = "postgresql+psycopg2"
    SQLALCHEMY_REDSHFIFT = "postgresql+psycopg2"

    DB_USER = os.environ.get("DB_USER", "n8n")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "n8npass")
    DB_HOST = os.environ.get("DB_HOST", "db:5432")
    DB_NAME = os.environ.get("DB_NAME", "n8ndb")

    DB_SCHEMA = os.environ.get("DB_SCHEMA", "public")

    TIMEOUT_RECONNECT_POSTGRE = int(os.getenv('TIMEOUT_RECONNECT_POSTGRE', 30))
    AMOUNT_PROCESS_API = int(os.environ.get("AMOUNT_PROCESS_API", 1))
    POLL_SIZE_POSTGRE = int(os.getenv('POLL_SIZE_POSTGRE', 30))
    PORT_API = os.environ.get("PORT_API", 9000)

    MIGRATION_USER = os.environ.get("MIGRATION_USER", "n8n")
    MIGRATION_PASSWORD = os.environ.get("MIGRATION_PASSWORD", "n8npass")

    @classmethod
    def connection_string(cls):
        return f"{cls.SQLALCHEMY_PREFIX}://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}/{cls.DB_NAME}"

    @classmethod
    def connection_string_migration(cls):
        return f"{cls.SQLALCHEMY_PREFIX}://{cls.MIGRATION_USER}:{cls.MIGRATION_PASSWORD}@{cls.DB_HOST}/{cls.DB_NAME}"