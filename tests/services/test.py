import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqqt.models import Base, Services
from tqqt.routers.services.crud import get_service, create_service, update_service, delete_service
from tqqt.routers.services.schemas import ServiceCreate, ServiceUpdate

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


def test_create_service(db):
    service_data = ServiceCreate(
        service_name="Test Service",
        image="test_image.png",
        short_description="This is a test service.",
        full_info_link="http://testservice.com"
    )
    service = create_service(db=db, service=service_data)
    assert service.service_name == "Test Service"
    assert service.image == "test_image.png"
    assert service.short_description == "This is a test service."
    assert service.full_info_link == "http://testservice.com"


def test_get_service(db):
    service = get_service(db, service_id=1)
    assert service is not None
    assert service.service_name == "Test Service"


def test_update_service(db):
    service_data = ServiceUpdate(
        service_name="Updated Service",
        image="updated_image.png",
        short_description="This is an updated test service.",
        full_info_link="http://updatedservice.com"
    )
    service = update_service(db=db, service_id=1, service=service_data)
    assert service.service_name == "Updated Service"
    assert service.image == "updated_image.png"
    assert service.short_description == "This is an updated test service."
    assert service.full_info_link == "http://updatedservice.com"


def test_delete_service(db):
    service = delete_service(db=db, service_id=1)
    assert service is not None
    assert service.service_name == "Updated Service"


def test_get_non_existent_service(db):
    service = get_service(db, service_id=999)
    assert service is None
