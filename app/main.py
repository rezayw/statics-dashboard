from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import config
from app.routes import upload
from app.db import base
from app.routes import auth
from app.routes import admin

app = FastAPI(title=config.APP_NAME)

app.include_router(upload.router, prefix=config.API_PREFIX, tags=["Upload"])
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router, prefix=config.API_PREFIX, tags=["Auth"])
app.include_router(admin.router, prefix=config.API_PREFIX, tags=["Admin"])

base.Base.metadata.create_all(bind=base.engine)