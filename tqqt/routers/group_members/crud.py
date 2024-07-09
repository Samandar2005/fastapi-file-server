from sqlalchemy.orm import Session
from datetime import datetime
from tqqt import models
from . import schemas


def get_group_member(db: Session, group_id: int, member_id: int):
    return db.query(models.GroupMembers).filter(
        models.GroupMembers.group_id == group_id,
        models.GroupMembers.member_id == member_id
    ).first()


def get_all_group_members(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.GroupMembers).offset(skip).limit(limit).all()


def create_group_member(db: Session, group_member: schemas.GroupMemberCreate):
    db_group_member = models.GroupMembers(
        group_id=group_member.group_id,
        member_id=group_member.member_id,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    db.add(db_group_member)
    db.commit()
    db.refresh(db_group_member)
    return db_group_member


def delete_group_member(db: Session, group_id: int, member_id: int):
    db_group_member = get_group_member(db, group_id, member_id)
    if db_group_member is None:
        return None
    db.delete(db_group_member)
    db.commit()
    return db_group_member
