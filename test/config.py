from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from starlette.testclient import TestClient

from app import model, main
from app.database import get_db


def set_test_db_client():
    SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:admin@localhost/fastapidemo_test"

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    if not database_exists(engine.url):
        create_database(engine.url)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()
    # model.Base.metadata.drop_all(engine)
    model.Base.metadata.create_all(bind=engine)

    # Override db
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    main.app.dependency_overrides[get_db] = override_get_db
    client = TestClient(main.app)
    return client
