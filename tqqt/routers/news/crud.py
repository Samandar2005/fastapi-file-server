from sqlalchemy.orm import Session
from . import schemas
from datetime import datetime
from tqqt import models


def get_news(db: Session, news_id: int):
    return db.query(models.News).filter(models.News.id == news_id).first()


def get_all_news(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.News).offset(skip).limit(limit).all()


def create_news(db: Session, news: schemas.NewsCreate):
    db_news = models.News(**news.dict(), created_date=datetime.utcnow(), updated_date=datetime.utcnow())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


def update_news(db: Session, news_id: int, news: schemas.NewsCreate):
    db_news = get_news(db, news_id)
    if db_news is None:
        return None
    for key, value in news.dict().items():
        setattr(db_news, key, value)
    db_news.updated_date = datetime.utcnow()
    db.commit()
    db.refresh(db_news)
    return db_news


def delete_news(db: Session, news_id: int):
    db_news = get_news(db, news_id)
    if db_news is None:
        return None
    db.delete(db_news)
    db.commit()
    return db_news

