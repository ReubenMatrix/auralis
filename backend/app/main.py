from fastapi import FastAPI # type: ignore
from app.routes import router
from app.repository.db import Base, engine

app = FastAPI()
Base.metadata.create_all(bind = engine)
app.include_router(router)

@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀"}
