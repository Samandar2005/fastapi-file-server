import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqqt.models import Base, Projects
from tqqt.routers.projects.crud import get_project, create_project, update_project, delete_project
from tqqt.routers.projects.schemas import ProjectCreate, ProjectUpdate
from datetime import date

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()


def test_create_project(db):
    project_data = ProjectCreate(
        title="Test Project",
        body="This is a test project body.",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        logo="test_logo.png",
    )
    project = create_project(db=db, project=project_data)
    assert project.title == "Test Project"
    assert project.body == "This is a test project body."
    assert project.start_date == date(2024, 1, 1)
    assert project.end_date == date(2024, 12, 31)
    assert project.logo == "test_logo.png"


def test_get_project(db):
    project = get_project(db, project_id=1)
    assert project is not None
    assert project.title == "Test Project"


def test_update_project(db):
    project_data = ProjectUpdate(
        title="Updated Project",
        body="This is an updated test project body.",
        start_date=date(2024, 2, 1),
        end_date=date(2024, 11, 30),
        logo="updated_logo.png",
    )
    project = update_project(db=db, project_id=1, project=project_data)
    assert project.title == "Updated Project"
    assert project.body == "This is an updated test project body."
    assert project.start_date == date(2024, 2, 1)
    assert project.end_date == date(2024, 11, 30)
    assert project.logo == "updated_logo.png"


def test_delete_project(db):
    project = delete_project(db=db, project_id=1)
    assert project is not None
    assert project.title == "Updated Project"


def test_get_non_existent_project(db):
    project = get_project(db, project_id=999)
    assert project is None
