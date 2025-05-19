from fastapi import FastAPI
from app import user, note
from app.database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix="/api")
app.include_router(note.router, prefix="/api")