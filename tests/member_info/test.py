import pytest
from tqqt import models
from tqqt.routers.member_info import schemas
from tqqt.routers.member_info.crud import *
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


def test_create_member_info(db_session):
    member_info_data = schemas.MemberInfoCreate(
        first_name="John",
        last_name="Doe",
        title="Developer",
        member_id=1,
        description="A skilled developer."
    )
    db_member_info = create_member_info(db_session, member_info_data)
    assert db_member_info.first_name == "John"
    assert db_member_info.last_name == "Doe"
    assert db_member_info.title == "Developer"
    assert db_member_info.member_id == 1
    assert db_member_info.description == "A skilled developer."


def test_get_member_info(db_session):
    db_member_info = get_member_info(db_session, 1)
    assert db_member_info is not None
    assert db_member_info.first_name == "John"
    assert db_member_info.last_name == "Doe"


def test_get_all_member_info(db_session):
    member_infos = get_all_member_info(db_session)
    assert len(member_infos) > 0


def test_update_member_info(db_session):
    member_info_data = schemas.MemberInfoCreate(
        first_name="Jane",
        last_name="Doe",
        title="Senior Developer",
        member_id=1,
        description="An experienced developer."
    )
    updated_member_info = update_member_info(db_session, 1, member_info_data)
    assert updated_member_info.first_name == "Jane"
    assert updated_member_info.last_name == "Doe"
    assert updated_member_info.title == "Senior Developer"
    assert updated_member_info.description == "An experienced developer."


def test_delete_member_info(db_session):
    deleted_member_info = delete_member_info(db_session, 1)
    assert deleted_member_info is not None
    db_member_info = get_member_info(db_session, 1)
    assert db_member_info is None
