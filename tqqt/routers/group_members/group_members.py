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


@router.post("/", response_model=schemas.GroupMember)
def create_group_member(group_member: schemas.GroupMemberCreate, db: Session = Depends(get_db)):
    return crud.create_group_member(db=db, group_member=group_member)


@router.get("/{group_id}/{member_id}", response_model=schemas.GroupMember)
def read_group_member(group_id: int, member_id: int, db: Session = Depends(get_db)):
    db_group_member = crud.get_group_member(db, group_id=group_id, member_id=member_id)
    if db_group_member is None:
        raise HTTPException(status_code=404, detail="Group member not found")
    return db_group_member


@router.get("/", response_model=List[schemas.GroupMember])
def read_group_members(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    group_members = crud.get_all_group_members(db, skip=skip, limit=limit)
    return group_members


@router.delete("/{group_id}/{member_id}", response_model=schemas.GroupMember)
def delete_group_member(group_id: int, member_id: int, db: Session = Depends(get_db)):
    db_group_member = crud.delete_group_member(db, group_id=group_id, member_id=member_id)
    if db_group_member is None:
        raise HTTPException(status_code=404, detail="Group member not found")
    return db_group_member
