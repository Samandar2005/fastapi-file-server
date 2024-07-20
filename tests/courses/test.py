import pytest
from tqqt import models
from tqqt.routers.courses import schemas
from tqqt.routers.courses.crud import create_course, get_course, get_all_courses, update_course, delete_course
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


def test_create_course(db_session):
    course_data = schemas.CourseCreate(
        title="Test Course",
        short_description="This is a test course.",
        logo="test_logo.png",
        edu_link="http://example.com"
    )
    db_course = create_course(db_session, course_data)
    assert db_course.title == "Test Course"
    assert db_course.short_description == "This is a test course."
    assert db_course.logo == "test_logo.png"
    assert db_course.edu_link == "http://example.com"


def test_get_course(db_session):
    db_course = get_course(db_session, 1)
    assert db_course is not None
    assert db_course.title == "Test Course"


def test_get_all_courses(db_session):
    courses = get_all_courses(db_session)
    assert len(courses) > 0


def test_update_course(db_session):
    course_data = schemas.CourseCreate(
        title="Updated Course",
        short_description="This is an updated test course.",
        logo="updated_logo.png",
        edu_link="http://example.com/updated"
    )
    updated_course = update_course(db_session, 1, course_data)
    assert updated_course.title == "Updated Course"
    assert updated_course.short_description == "This is an updated test course."
    assert updated_course.logo == "updated_logo.png"
    assert updated_course.edu_link == "http://example.com/updated"


def test_delete_course(db_session):
    deleted_course = delete_course(db_session, 1)
    assert deleted_course is not None
    db_course = get_course(db_session, 1)
    assert db_course is None
