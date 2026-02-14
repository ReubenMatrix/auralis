from fastapi import FastAPI, Depends
from app.routes.song_routes import router as song_router
from app.repository.db import Base, engine
from sqlalchemy.orm import Session
from app.repository.db import init_db 

app = FastAPI()
Base.metadata.create_all(bind = engine)
app.include_router(song_router)

@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀"}


@app.get("/health")
def health(db: Session = Depends(init_db)):
    return {"status": "db connected"}
