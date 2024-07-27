from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from tqqt import models
from tqqt.database import SessionLocal, engine
from . import crud, schemas


models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.News)
def create_news(news: schemas.NewsCreate, db: Session = Depends(get_db)):
    return crud.create_news(db=db, news=news)


@router.get("/{news_id}", response_model=schemas.News)
def read_news(news_id: int, db: Session = Depends(get_db)):
    db_news = crud.get_news(db, news_id=news_id)
    if db_news is None:
        raise HTTPException(status_code=404, detail="News not found")
    return db_news


@router.get("/", response_model=List[schemas.News])
def read_news(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    news = crud.get_all_news(db, skip=skip, limit=limit)
    return news


@router.put("/{news_id}", response_model=schemas.News)
def update_news(news_id: int, news: schemas.NewsCreate, db: Session = Depends(get_db)):
    db_news = crud.update_news(db, news_id=news_id, news=news)
    if db_news is None:
        raise HTTPException(status_code=404, detail="News not found")
    return db_news


@router.delete("/{news_id}", response_model=schemas.News)
def delete_news(news_id: int, db: Session = Depends(get_db)):
    db_news = crud.delete_news(db, news_id=news_id)
    if db_news is None:
        raise HTTPException(status_code=404, detail="News not found")
    return db_news
