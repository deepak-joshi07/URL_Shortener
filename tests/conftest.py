import os 
import pytest
from dotenv import load_dotenv
from sqlalchemy.engine import make_url
from sqlmodel import SQLModel , Session , create_engine
from app.database.db import get_session
from app.routes import app

load_dotenv(".env.test" , override=True)

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "TEST_DATABASE_URL is missing. "
        "Configure it in .env.test."
    )

database_name = make_url(TEST_DATABASE_URL).database

if not database_name or not database_name.endswith("_test"):
    raise RuntimeError(
        "Refusing to run tests: the database name "
        "must end with '_test'."
    )


from app.database.models import Link , User

@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DATABASE_URL)

    SQLModel.metadata.create_all(engine)

    yield engine

    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()

    test_session = Session(
        bind = connection , 
        join_transaction_mode="create_savepoint",
    )

    try:
        yield test_session
    finally:
        test_session.close()

        if transaction.is_active:
            transaction.rollback()

        connection.close()


@pytest.fixture
def test_user(session):
    user = User(
        user_id=1974386250918473728,
        username="testuser",
        email="testuser@example.com",
        hashed_password="test_hash",
    )

    session.add(user)
    session.flush()

    return user

@pytest.fixture
def test_link(session , test_user):
    link_id = 712953508182743859
    short_code = 'qfKkK1W9rf'
    url = "https://www.youtube.com/" 

    link = Link(
        original_url= url , 
        user_id= test_user.user_id,
        link_id= link_id,
        short_code= short_code
    )

    session.add(link)
    session.flush()

    return link




@pytest.fixture
def override_get_session(session):
        def override_helper():
            return session

        app.dependency_overrides[get_session] = override_helper

        yield
        
        app.dependency_overrides.pop(get_session, None)
