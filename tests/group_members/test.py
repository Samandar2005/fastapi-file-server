import pytest
from tqqt import models
from tqqt.routers.group_members import schemas
from tqqt.routers.group_members.crud import create_group_member, get_group_member, get_all_group_members, \
    delete_group_member
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

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


def test_create_group_member(db_session):
    group_member_data = schemas.GroupMemberCreate(
        group_id=1,
        member_id=1,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    db_group_member = create_group_member(db_session, group_member_data)
    assert db_group_member.group_id == 1
    assert db_group_member.member_id == 1


def test_get_group_member(db_session):
    db_group_member = get_group_member(db_session, 1, 1)
    assert db_group_member is not None
    assert db_group_member.group_id == 1
    assert db_group_member.member_id == 1


def test_get_all_group_members(db_session):
    group_members = get_all_group_members(db_session)
    assert len(group_members) > 0


def test_delete_group_member(db_session):
    deleted_group_member = delete_group_member(db_session, 1, 1)
    assert deleted_group_member is not None
    db_group_member = get_group_member(db_session, 1, 1)
    assert db_group_member is None
