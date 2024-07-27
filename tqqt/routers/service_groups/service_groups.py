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


@router.post("/", response_model=schemas.ServiceGroup)
def create_service_group(service_group: schemas.ServiceGroupCreate, db: Session = Depends(get_db)):
    return crud.create_service_group(db=db, service_group=service_group)


@router.get("/{service_group_id}", response_model=schemas.ServiceGroup)
def read_service_group(service_group_id: int, db: Session = Depends(get_db)):
    db_service_group = crud.get_service_group(db, service_group_id=service_group_id)
    if db_service_group is None:
        raise HTTPException(status_code=404, detail="Service group not found")
    return db_service_group


@router.get("/", response_model=List[schemas.ServiceGroup])
def read_service_groups(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    service_groups = crud.get_all_service_groups(db, skip=skip, limit=limit)
    return service_groups


@router.put("/{service_group_id}", response_model=schemas.ServiceGroup)
def update_service_group(service_group_id: int, service_group: schemas.ServiceGroupCreate,
                         db: Session = Depends(get_db)):
    db_service_group = crud.update_service_group(db, service_group_id=service_group_id, service_group=service_group)
    if db_service_group is None:
        raise HTTPException(status_code=404, detail="Service group not found")
    return db_service_group


@router.delete("/{service_group_id}", response_model=schemas.ServiceGroup)
def delete_service_group(service_group_id: int, db: Session = Depends(get_db)):
    db_service_group = crud.delete_service_group(db, service_group_id=service_group_id)
    if db_service_group is None:
        raise HTTPException(status_code=404, detail="Service group not found")
    return db_service_group
