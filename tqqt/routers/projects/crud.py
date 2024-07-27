from sqlalchemy.orm import Session
from . import schemas
from tqqt import models


def get_project(db: Session, project_id: int):
    return db.query(models.Projects).filter(models.Projects.id == project_id).first()


def get_all_projects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Projects).offset(skip).limit(limit).all()


def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Projects(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project: schemas.ProjectCreate):
    db_project = get_project(db, project_id)
    if db_project is None:
        return None
    for key, value in project.dict().items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    if db_project is None:
        return None
    db.delete(db_project)
    db.commit()
    return db_project
