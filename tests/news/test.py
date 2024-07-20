import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqqt.models import Base, News
from tqqt.routers.news.crud import get_news, create_news, update_news, delete_news
from tqqt.routers.news.schemas import NewsCreate, NewsUpdate

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


def test_create_news(db):
    news_data = NewsCreate(
        title="Test News",
        logo="test_logo.png",
        full_text="This is a test news article.",
    )
    news_item = create_news(db=db, news=news_data)
    assert news_item.title == "Test News"
    assert news_item.logo == "test_logo.png"
    assert news_item.full_text == "This is a test news article."


def test_get_news(db):
    news_item = get_news(db, news_id=1)
    assert news_item is not None
    assert news_item.title == "Test News"


def test_update_news(db):
    news_data = NewsUpdate(
        title="Updated News",
        logo="updated_logo.png",
        full_text="This is an updated test news article.",
    )
    news_item = update_news(db=db, news_id=1, news=news_data)
    assert news_item.title == "Updated News"
    assert news_item.logo == "updated_logo.png"
    assert news_item.full_text == "This is an updated test news article."


def test_delete_news(db):
    news_item = delete_news(db=db, news_id=1)
    assert news_item is not None
    assert news_item.title == "Updated News"


def test_get_non_existent_news(db):
    news_item = get_news(db, news_id=999)
    assert news_item is None
