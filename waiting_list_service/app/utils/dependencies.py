from app.managers.postgres_manager import PostgresManager
from app.utils.config import get_settings

def get_postgres_manager():
    postgres_manager = PostgresManager(
        host=get_settings().postgres_hostname,
        port=get_settings().postgres_port,
        dbname=get_settings().postgres_db,
        user=get_settings().postgres_user,
        password=get_settings().postgres_password
    )
    try:
        yield postgres_manager
    finally:
        pass
