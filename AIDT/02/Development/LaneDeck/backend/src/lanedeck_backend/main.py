from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import configure_database, get_engine, init_db, is_configured
from .routes import router


def create_app(database_url: str | None = None) -> FastAPI:
    if database_url is not None:
        configure_database(database_url)
    elif not is_configured():
        configure_database()
    init_db(get_engine())

    app = FastAPI(title="LaneDeck API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:5173",
            "http://localhost:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app
