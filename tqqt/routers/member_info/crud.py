from sqlalchemy.orm import Session
from datetime import datetime
from .schemas import MemberInfoCreate
from tqqt.models import MemberInfo


def get_member_info(db: Session, member_info_id: int):
    return db.query(MemberInfo).filter(MemberInfo.id == member_info_id).first()


def get_all_member_info(db: Session, skip: int = 0, limit: int = 10):
    return db.query(MemberInfo).offset(skip).limit(limit).all()


def create_member_info(db: Session, member_info: MemberInfoCreate):
    db_member_info = MemberInfo(**member_info.dict(), created_date=datetime.utcnow(), updated_date=datetime.utcnow())
    db.add(db_member_info)
    db.commit()
    db.refresh(db_member_info)
    return db_member_info


def update_member_info(db: Session, member_info_id: int, member_info: MemberInfoCreate):
    db_member_info = get_member_info(db, member_info_id)
    if db_member_info is None:
        return None
    for key, value in member_info.dict().items():
        setattr(db_member_info, key, value)
    db_member_info.updated_date = datetime.utcnow()
    db.commit()
    db.refresh(db_member_info)
    return db_member_info


def delete_member_info(db: Session, member_info_id: int):
    db_member_info = get_member_info(db, member_info_id)
    if db_member_info is None:
        return None
    db.delete(db_member_info)
    db.commit()
    return db_member_info
