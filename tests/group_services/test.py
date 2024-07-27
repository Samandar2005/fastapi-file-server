import pytest
from tqqt import models
from tqqt.routers.group_services import schemas
from tqqt.routers.group_services.crud import create_group_service, get_group_service, get_all_group_services, delete_group_service
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_group_service(db_session):
    group_service_data = schemas.GroupServicesCreate(
        group_id=1,
        service_id=1
    )
    db_group_service = create_group_service(db_session, group_service_data)
    assert db_group_service.group_id == 1
    assert db_group_service.service_id == 1


def test_get_group_service(db_session):
    db_group_service = get_group_service(db_session, 1, 1)
    assert db_group_service is not None
    assert db_group_service.group_id == 1
    assert db_group_service.service_id == 1


def test_get_all_group_services(db_session):
    group_services = get_all_group_services(db_session)
    assert len(group_services) > 0


def test_delete_group_service(db_session):
    deleted_group_service = delete_group_service(db_session, 1, 1)
    assert deleted_group_service is not None
    db_group_service = get_group_service(db_session, 1, 1)
    assert db_group_service is None
