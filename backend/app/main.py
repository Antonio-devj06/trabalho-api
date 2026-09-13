from fastapi import FastAPI

from app.database import engine
from app.database import Base

from app.routes.viagens import router as viagens_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Viagens"
)

import os

@app.get("/instance")
def instance():
    return {
        "instance": os.getenv("HOSTNAME")
    }

app.include_router(viagens_router)