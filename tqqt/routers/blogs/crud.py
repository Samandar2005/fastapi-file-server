from sqlalchemy.orm import Session
from datetime import datetime
from tqqt import models
from . import schemas


def get_blog(db: Session, blog_id: int):
    return db.query(models.Blogs).filter(models.Blogs.id == blog_id).first()


def get_all_blogs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Blogs).offset(skip).limit(limit).all()


def create_blog(db: Session, blog: schemas.BlogCreate):
    db_blog = models.Blogs(
        **blog.dict(),
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


def update_blog(db: Session, blog_id: int, blog: schemas.BlogCreate):
    db_blog = get_blog(db, blog_id)
    if db_blog is None:
        return None
    for key, value in blog.dict().items():
        setattr(db_blog, key, value)
    db_blog.updated_date = datetime.utcnow()
    db.commit()
    db.refresh(db_blog)
    return db_blog


def delete_blog(db: Session, blog_id: int):
    db_blog = get_blog(db, blog_id)
    if db_blog is None:
        return None
    db.delete(db_blog)
    db.commit()
    return db_blog
