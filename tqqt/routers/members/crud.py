from sqlalchemy.orm import Session
from .schemas import Member, MemberCreate
from datetime import datetime


def get_member(db: Session, member_id: int):
    return db.query(Member).filter(Member.id == member_id).first()


def get_all_members(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Member).offset(skip).limit(limit).all()


def create_member(db: Session, member: MemberCreate):
    db_member = Member(**member.dict(), created_date=datetime.utcnow(), updated_date=datetime.utcnow())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def update_member(db: Session, member_id: int, member: MemberCreate):
    db_member = get_member(db, member_id)
    if db_member is None:
        return None
    for key, value in member.dict().items():
        setattr(db_member, key, value)
    db_member.updated_date = datetime.utcnow()
    db.commit()
    db.refresh(db_member)
    return db_member


def delete_member(db: Session, member_id: int):
    db_member = get_member(db, member_id)
    if db_member is None:
        return None
    db.delete(db_member)
    db.commit()
    return db_member
