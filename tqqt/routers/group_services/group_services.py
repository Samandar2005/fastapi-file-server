from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from tqqt import models
from tqqt.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.GroupServices)
def create_group_service(group_service: schemas.GroupServicesCreate, db: Session = Depends(get_db)):
    return crud.create_group_service(db=db, group_service=group_service)


@router.get("/", response_model=List[schemas.GroupServices])
def read_group_services(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_group_services(db, skip=skip, limit=limit)


@router.delete("/{group_id}/{service_id}", response_model=schemas.GroupServices)
def delete_group_service(group_id: int, service_id: int, db: Session = Depends(get_db)):
    deleted_group_service = crud.delete_group_service(db, group_id, service_id)
    if deleted_group_service is None:
        raise HTTPException(status_code=404, detail="Group service not found")
    return deleted_group_service
