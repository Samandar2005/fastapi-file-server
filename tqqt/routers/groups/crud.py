from sqlalchemy.orm import Session
from .schemas import GroupCreate
from datetime import datetime
from tqqt.models import Groups


def get_group(db: Session, group_id: int):
    return db.query(Groups).filter(Groups.id == group_id).first()


def get_all_groups(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Groups).offset(skip).limit(limit).all()


def create_group(db: Session, group: GroupCreate):
    db_group = Groups(**group.dict(), created_date=datetime.utcnow(), updated_date=datetime.utcnow())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def update_group(db: Session, group_id: int, group: GroupCreate):
    db_group = get_group(db, group_id)
    if db_group is None:
        return None
    for key, value in group.dict().items():
        setattr(db_group, key, value)
    db_group.updated_date = datetime.utcnow()
    db.commit()
    db.refresh(db_group)
    return db_group


def delete_group(db: Session, group_id: int):
    db_group = get_group(db, group_id)
    if db_group is None:
        return None
    db.delete(db_group)
    db.commit()
    return db_group
