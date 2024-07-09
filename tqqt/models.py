from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    logo = Column(String)
    full_text = Column(Text)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)


class Groups(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    logo = Column(String)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)


class Members(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    image = Column(String)
    short_description = Column(Text)
    full_info_link = Column(String)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)


class MemberInfo(Base):
    __tablename__ = "member_info"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    title = Column(String)
    member_id = Column(Integer, ForeignKey("members.id"))
    description = Column(Text)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)
    member = relationship("Members")


class GroupMembers(Base):
    __tablename__ = "group_members"
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), primary_key=True)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)


class Projects(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    logo = Column(String)


class Blogs(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    short_info = Column(Text)
    logo = Column(String)
    blog_link = Column(String)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)


class Courses(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    short_description = Column(Text)
    logo = Column(String)
    edu_link = Column(String)


class ServiceGroups(Base):
    __tablename__ = "service_groups"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    logo = Column(String)


class Services(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, index=True)
    image = Column(String)
    short_description = Column(Text)
    full_info_link = Column(String)


class GroupServices(Base):
    __tablename__ = "group_services"
    group_id = Column(Integer, ForeignKey("service_groups.id"), primary_key=True)
    service_id = Column(Integer, ForeignKey("services.id"), primary_key=True)
