import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db.connection import Base, SessionLocal, engine
from .db.migrate import migrate
from .question_bank.seed import seed
from .routers import auth, dashboard, home, profile, quiz_sessions

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    migrate(engine)
    with SessionLocal() as db:
        seed(db)
    yield


app = FastAPI(title="Pattern Quiz API", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(home.router)
app.include_router(quiz_sessions.router)
app.include_router(dashboard.router)


@app.get("/api/health")
def health():
    return {"ok": True}
