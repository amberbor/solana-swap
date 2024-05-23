from database.connections import BaseDatabaseManager
from sqlalchemy.exc import IntegrityError
from custom_logger import logger


class DatabaseManager(BaseDatabaseManager):
    def insert_record(self, new_record):
        with self as db:
            self.session.add(new_record)
            try:
                self.session.commit()
                self.session.refresh(new_record)
                return new_record
            except IntegrityError as e:
                logger.error(e)

            except Exception as e:
                self.session.rollback()
                logger.error(e)

    def get_last_record(self, entity, order_by_field="created_at", **filters):
        with self as db:
            record = (
                self.session.query(entity)
                .filter_by(**filters)
                .order_by(getattr(entity, order_by_field).desc())
                .first()
            )
            return record

    def get_records(self, entity, order_by_field, **filters):
        with self as db:
            records = (
                self.session.query(entity)
                .filter_by(**filters)
                .order_by(getattr(entity, order_by_field))
            )
            return records

    def get_record(self, entity, **filters):
        with self as db:
            record = self.session.query(entity).filter_by(**filters).first()
            return record

    def get_all(self, entity, order_by_field="created_at", **filters):
        with self as db:
            return (
                self.session.query(entity)
                .filter_by(**filters)
                .order_by(getattr(entity, order_by_field))
                .all()
            )

    def update_records(self):
        with self as db:
            try:
                self.session.commit()
            except IntegrityError as e:
                return None
            except Exception as e:
                self.session.rollback()
                raise e
