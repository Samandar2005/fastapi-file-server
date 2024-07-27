import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqqt.models import Base
from tqqt.routers.members import schemas
from tqqt.routers.members.crud import get_member, get_all_members, create_member, update_member, delete_member

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_member(db):
    member_data = schemas.MemberCreate(
        full_name="Test Member",
        image="test_image.png",
        short_description="This is a test member",
        full_info_link="http://testmember.com"
    )
    member = create_member(db, member_data)
    assert member.id is not None
    assert member.full_name == "Test Member"
    assert member.image == "test_image.png"
    assert member.short_description == "This is a test member"
    assert member.full_info_link == "http://testmember.com"
    assert member.created_date is not None
    assert member.updated_date is not None


def test_get_member(db):
    member = get_member(db, 1)
    assert member is not None
    assert member.full_name == "Test Member"
    assert member.image == "test_image.png"
    assert member.short_description == "This is a test member"
    assert member.full_info_link == "http://testmember.com"


def test_get_all_members(db):
    members = get_all_members(db)
    assert len(members) == 1
    assert members[0].full_name == "Test Member"


def test_update_member(db):
    member_data = schemas.MemberCreate(
        full_name="Updated Member",
        image="updated_image.png",
        short_description="This is an updated test member",
        full_info_link="http://updatedmember.com"
    )
    member = update_member(db, 1, member_data)
    assert member is not None
    assert member.full_name == "Updated Member"
    assert member.image == "updated_image.png"
    assert member.short_description == "This is an updated test member"
    assert member.full_info_link == "http://updatedmember.com"
    assert member.created_date is not None
    assert member.updated_date is not None


def test_delete_member(db):
    member = delete_member(db, 1)
    assert member is not None
    member = get_member(db, 1)
    assert member is None
