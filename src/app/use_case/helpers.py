from src.app.services.database import DatabaseManager
from src.database.orm import Configurations

def get_configurations(db_manager: DatabaseManager):
    with db_manager as db:
        return db.get_last_record(entity = Configurations, order_by_field='created_at')
