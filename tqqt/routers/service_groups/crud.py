from sqlalchemy.orm import Session
from . import schemas
from tqqt import models


def get_service_group(db: Session, service_group_id: int):
    return db.query(models.ServiceGroups).filter(models.ServiceGroups.id == service_group_id).first()


def get_all_service_groups(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ServiceGroups).offset(skip).limit(limit).all()


def create_service_group(db: Session, service_group: schemas.ServiceGroupCreate):
    db_service_group = models.ServiceGroups(
        title=service_group.title,
        logo=service_group.logo
    )
    db.add(db_service_group)
    db.commit()
    db.refresh(db_service_group)
    return db_service_group


def update_service_group(db: Session, service_group_id: int, service_group: schemas.ServiceGroupCreate):
    db_service_group = get_service_group(db, service_group_id)
    if db_service_group is None:
        return None
    for key, value in service_group.dict().items():
        setattr(db_service_group, key, value)
    db.commit()
    db.refresh(db_service_group)
    return db_service_group


def delete_service_group(db: Session, service_group_id: int):
    db_service_group = get_service_group(db, service_group_id)
    if db_service_group is None:
        return None
    db.delete(db_service_group)
    db.commit()
    return db_service_group
