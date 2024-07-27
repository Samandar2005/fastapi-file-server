from fastapi import FastAPI
from .routers.news import news
from .routers.groups import groups
from .routers.members import members
from .routers.member_info import member_info
from .routers.projects import projects
from .routers.group_members import group_members
from .routers.blogs import blogs
from .routers.courses import courses
from .routers.service_groups import service_groups
from .routers.services import services
from .routers.group_services import group_services
from . import root
from fastapi import FastAPI

app = FastAPI()

app.include_router(root.router, prefix="", tags=["root"])
app.include_router(news.router, prefix="/news", tags=["news"])
app.include_router(groups.router, prefix="/groups", tags=["groups"])
app.include_router(members.router, prefix="/members", tags=["members"])
app.include_router(member_info.router, prefix="/member_info", tags=["member_info"])
app.include_router(group_members.router, prefix="/group_members", tags=["group_members"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(blogs.router, prefix="/blogs", tags=["blogs"])
app.include_router(courses.router, prefix="/courses", tags=["courses"])
app.include_router(service_groups.router, prefix="/service_groups", tags=["service_groups"])
app.include_router(services.router, prefix="/services", tags=["services"])
app.include_router(group_services.router, prefix="/group_services", tags=["group_services"])
