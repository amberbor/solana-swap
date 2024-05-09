
from src.database.connections import BaseDatabaseManager
class DatabaseManager(BaseDatabaseManager):
    def insert_record(self, new_record):
        self.session.add(new_record)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollbac()
            raise e

    def get_last_record(self, entity, order_by_field , **filters):
        record = self.session.query(entity).filter_by(**filters).order_by(getattr(entity, order_by_field).desc()).first()
        return record

    def get_records(self, entity, order_by_field ,**filters):
        records = self.session.query(entity).filter_by(**filters).order_by(getattr(entity, order_by_field))
        return records