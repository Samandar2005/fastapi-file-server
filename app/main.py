from fastapi import FastAPI
from app.routers import file
from app.database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get('/')
async def root():
    return {"This is the main page!"}


app.include_router(file.router)
