import pytest
from tqqt import models
from tqqt.routers.groups import schemas
from tqqt.routers.groups.crud import create_group, get_group, get_all_groups, update_group, delete_group
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


def test_create_group(db_session):
    group_data = schemas.GroupCreate(
        title="Test Group",
        logo="test_logo.png"
    )
    group = create_group(db_session, group_data)
    assert group.id is not None
    assert group.title == "Test Group"
    assert group.logo == "test_logo.png"


def test_get_group(db_session):
    group = get_group(db_session, 1)
    assert group is not None
    assert group.title == "Test Group"
    assert group.logo == "test_logo.png"


def test_get_all_groups(db_session):
    groups = get_all_groups(db_session)
    assert len(groups) == 1
    assert groups[0].title == "Test Group"


def test_update_group(db_session):
    group_data = schemas.GroupCreate(
        title="Updated Group",
        logo="updated_logo.png"
    )
    group = update_group(db_session, 1, group_data)
    assert group is not None
    assert group.title == "Updated Group"
    assert group.logo == "updated_logo.png"


def test_delete_group(db_session):
    group = delete_group(db_session, 1)
    assert group is not None
    group = get_group(db_session, 1)
    assert group is None
