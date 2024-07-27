import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqqt.models import Base, ServiceGroups
from tqqt.routers.service_groups.crud import get_service_group, create_service_group, update_service_group, \
    delete_service_group
from tqqt.routers.service_groups.schemas import ServiceGroupCreate, ServiceGroupUpdate

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


def test_create_service_group(db):
    # Test creating a service group
    service_group_data = ServiceGroupCreate(
        title="Test Service Group",
        logo="test_logo.png",
    )
    service_group = create_service_group(db=db, service_group=service_group_data)
    assert service_group.title == "Test Service Group"
    assert service_group.logo == "test_logo.png"


def test_get_service_group(db):
    # Test retrieving a service group
    service_group = get_service_group(db, service_group_id=1)
    assert service_group is not None
    assert service_group.title == "Test Service Group"


def test_update_service_group(db):
    # Test updating a service group
    service_group_data = ServiceGroupUpdate(
        title="Updated Service Group",
        logo="updated_logo.png",
    )
    service_group = update_service_group(db=db, service_group_id=1, service_group=service_group_data)
    assert service_group.title == "Updated Service Group"
    assert service_group.logo == "updated_logo.png"


def test_delete_service_group(db):
    # Test deleting a service group
    service_group = delete_service_group(db=db, service_group_id=1)
    assert service_group is not None
    assert service_group.title == "Updated Service Group"


def test_get_non_existent_service_group(db):
    # Test retrieving a non-existent service group
    service_group = get_service_group(db, service_group_id=999)
    assert service_group is None
