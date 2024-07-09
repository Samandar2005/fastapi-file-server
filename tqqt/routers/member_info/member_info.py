from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
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


@router.post("/", response_model=schemas.MemberInfo)
def create_member_info(member_info: schemas.MemberInfoCreate, db: Session = Depends(get_db)):
    return crud.create_member_info(db=db, member_info=member_info)


@router.get("/{member_info_id}", response_model=schemas.MemberInfo)
def read_member_info(member_info_id: int, db: Session = Depends(get_db)):
    db_member_info = crud.get_member_info(db, member_info_id=member_info_id)
    if db_member_info is None:
        raise HTTPException(status_code=404, detail="MemberInfo not found")
    return db_member_info


@router.get("/", response_model=List[schemas.MemberInfo])
def read_member_infos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    member_infos = crud.get_all_member_info(db, skip=skip, limit=limit)
    return member_infos


@router.put("/{member_info_id}", response_model=schemas.MemberInfo)
def update_member_info(member_info_id: int, member_info: schemas.MemberInfoCreate, db: Session = Depends(get_db)):
    db_member_info = crud.update_member_info(db, member_info_id=member_info_id, member_info=member_info)
    if db_member_info is None:
        raise HTTPException(status_code=404, detail="MemberInfo not found")
    return db_member_info


@router.delete("/{member_info_id}", response_model=schemas.MemberInfo)
def delete_member_info(member_info_id: int, db: Session = Depends(get_db)):
    db_member_info = crud.delete_member_info(db, member_info_id=member_info_id)
    if db_member_info is None:
        raise HTTPException(status_code=404, detail="MemberInfo not found")
    return db_member_info
