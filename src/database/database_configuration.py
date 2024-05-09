
from src.configs import (
    POSTGRES_DB_NAME,
    POSTGRES_DB_HOST,
    POSTGRES_DB_USER,
    POSTGRES_DB_PASSWORD,
    POSTGRES_DB_PORT,
TEST
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def create_uri():
    return f"postgresql://{POSTGRES_DB_USER}:{POSTGRES_DB_PASSWORD}@{POSTGRES_DB_HOST}:{POSTGRES_DB_PORT}/{POSTGRES_DB_NAME}?sslmode=prefer"