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

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)


@pytest.fixture()
def db():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

#   CLIENT con override DB

@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

#   crea tabelle

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)



# 👤 USER
@pytest.fixture()
def test_user(db):
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
def test_workspace(db, test_user):
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
def test_membership(db, test_user, test_workspace):
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
def test_project(db, test_workspace, test_membership):
    project = Project(
        name="Test Project",
        workspace_id=test_workspace.id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project