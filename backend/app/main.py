from fastapi import FastAPI, Depends, status
from app.routes.song_routes import router as song_router
from app.db.base import Base, engine
from sqlalchemy.orm import Session
from app.db.base import init_db 
from app.core.logger import logger

app = FastAPI()
Base.metadata.create_all(bind = engine)
app.include_router(song_router)

@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀"}


@app.get("/health")
def health(db: Session = Depends(init_db)):
    return {"status": "db connected"}

@app.delete("/flush-redis", status_code=status.HTTP_200_OK)
def flush_redis():
    try:
        import redis
        import os

        r = redis.Redis.from_url(os.getenv("REDIS_URL"))
        r.flushall()

        return {"message": "Redis flushed successfully"}

    except Exception as e:
         return {"message": "Redis Not flushed successfully"}
        