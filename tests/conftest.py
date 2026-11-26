from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from macrotrack.database import engine, get_session
from macrotrack.main import app

test_engine = create_engine(engine.url.set(database="macrotrack_test"))

TestSessionFactory = sessionmaker(bind=test_engine)


def get_test_session() -> Iterator[Session]:
    with TestSessionFactory() as session:
        yield session


@pytest.fixture
def client() -> Iterator[TestClient]:
    app.dependency_overrides[get_session] = get_test_session

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_session, None)
