from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class MySqlConnection:
    SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:admin@localhost/fastapidemo"

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

    def get_db(self):
        try:
            db = self.SessionLocal()
            yield db
        finally:
            db.close()

class SQLiteConnection:
    SQLALCHEMY_DATABASE_URL = "sqlite:///db"

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

    def get_db(self):
        try:
            db = self.SessionLocal()
            yield db
        finally:
            db.close()

