import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.deps import get_db
from app.main import app

from fastapi.testclient import TestClient
import os
from app.models.user import User
from app.core.security import hash_password

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# crea database
Base.metadata.create_all(bind=engine)


# override dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture()
def test_user():
    db = next(override_get_db())

    user = db.query(User).filter(User.email == "massi7@test.com").first()

    if user:
        user.full_name = "Test User"
        user.hashed_password = hash_password("123456")
        user.is_active = True
        user.is_verified = True
        db.commit()
        db.refresh(user)
        return user

    user = User(
        email="massi7@test.com",
        full_name="Test User",
        hashed_password=hash_password("123456"),
        is_active=True,
        is_verified=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture()
def token(client, test_user):
    response = client.post(
        "/auth/login",
        json={
            "email": test_user.email,
            "password": "123456"
        }
    )

    return response.json()["access_token"]