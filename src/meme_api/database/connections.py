from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from meme_api.database.database_configuration import create_uri

class BaseDatabaseManager:
    def __init__(self):
        self.uri = create_uri()
        self.engine = create_engine(self.uri)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
        self.session = None

    def __enter__(self):
        self.session = self.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


    def insert_record(self, new_record):
        self.session.add(new_record)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollbac()
            raise e

    def get_last_record(self, entity, order_by_field , **filters):
        record = self.session.query(entity).filter_by(**filters).order_by(getattr(entity, order_by_field).desc())
        return record

    def get_records(self, entity, order_by_field ,**filters):
        records = self.session.query(entity).filter_by(**filters).order_by(getattr(entity, order_by_field))
        return records

