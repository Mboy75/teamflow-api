import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.deps import get_db
from app.models.user import User
from app.models.workspace import Workspace
from app.models.membership import Membership
from app.models.project import Project
from app.core.security import hash_password

# SQLite in-memory
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    return TestClient(app)


# 👤 USER
@pytest.fixture()
def test_user():
    db = next(override_get_db())

    user = db.query(User).filter(User.email == "test@example.com").first()

    if user:
        return user

    user = User(
        email="test@example.com",
        full_name="Test User",
        hashed_password=hash_password("123456"),
        is_active=True,
        is_verified=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# 🔐 TOKEN
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


# 🏢 WORKSPACE
@pytest.fixture()
def test_workspace(test_user):
    db = next(override_get_db())

    workspace = Workspace(
        name="Test Workspace",
        slug="test-workspace",
        owner_id=test_user.id
    )

    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    return workspace


# 👥 MEMBERSHIP
@pytest.fixture()
def test_membership(test_user, test_workspace):
    db = next(override_get_db())

    membership = Membership(
        user_id=test_user.id,
        workspace_id=test_workspace.id,
        role="owner"
    )

    db.add(membership)
    db.commit()
    db.refresh(membership)

    return membership


# 📦 PROJECT
@pytest.fixture()
def test_project(test_workspace, test_membership):
    db = next(override_get_db())

    project = Project(
        name="Test Project",
        workspace_id=test_workspace.id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project