from sqlalchemy.orm import Session
from tqqt import models
from . import schemas


def get_group_service(db: Session, group_id: int, service_id: int):
    return db.query(models.GroupServices).filter(
        models.GroupServices.group_id == group_id,
        models.GroupServices.service_id == service_id
    ).first()


def get_all_group_services(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.GroupServices).offset(skip).limit(limit).all()


def create_group_service(db: Session, group_service: schemas.GroupServicesCreate):
    db_group_service = models.GroupServices(
        group_id=group_service.group_id,
        service_id=group_service.service_id
    )
    db.add(db_group_service)
    db.commit()
    db.refresh(db_group_service)
    return db_group_service


def delete_group_service(db: Session, group_id: int, service_id: int):
    db_group_service = get_group_service(db, group_id, service_id)
    if db_group_service:
        db.delete(db_group_service)
        db.commit()
        return db_group_service
    return None
