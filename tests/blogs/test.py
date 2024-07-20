import pytest
from tqqt import models
from tqqt.routers.blogs import schemas
from tqqt.routers.blogs.crud import get_blog, get_all_blogs, create_blog, update_blog, delete_blog
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_blog(db):
    blog_data = schemas.BlogCreate(
        title="Test Blog",
        short_info="This is a test blogs",
        logo="test_logo.png",
        blog_link="http://testblog.com"
    )
    blog = create_blog(db, blog_data)
    assert blog.id is not None
    assert blog.title == "Test Blog"
    assert blog.short_info == "This is a test blogs"
    assert blog.logo == "test_logo.png"
    assert blog.blog_link == "http://testblog.com"


def test_get_blog(db):
    blog = get_blog(db, 1)
    assert blog is not None
    assert blog.title == "Test Blog"
    assert blog.short_info == "This is a test blogs"
    assert blog.logo == "test_logo.png"
    assert blog.blog_link == "http://testblog.com"


def test_get_all_blogs(db):
    blogs = get_all_blogs(db)
    assert len(blogs) == 1
    assert blogs[0].title == "Test Blog"


def test_update_blog(db):
    blog_data = schemas.BlogCreate(
        title="Updated Blog",
        short_info="This is an updated test blogs",
        logo="updated_logo.png",
        blog_link="http://updatedblog.com"
    )
    blog = update_blog(db, 1, blog_data)
    assert blog is not None
    assert blog.title == "Updated Blog"
    assert blog.short_info == "This is an updated test blogs"
    assert blog.logo == "updated_logo.png"
    assert blog.blog_link == "http://updatedblog.com"


def test_delete_blog(db):
    blog = delete_blog(db, 1)
    assert blog is not None
    blog = get_blog(db, 1)
    assert blog is None
