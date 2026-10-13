from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

# Ensure data directory exists
if settings.DATABASE_URL.startswith("sqlite:///"):
    db_path = settings.DATABASE_URL.replace("sqlite:///", "", 1)
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args, future=True)

# Try to enable WAL for SQLite; if filesystem doesn't support it (e.g., Termux external storage), fall back safely
if settings.DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def _set_sqlite_pragma(dbapi_conn, _):
        try:
            cur = dbapi_conn.cursor()
            try:
                cur.execute("PRAGMA journal_mode=WAL;")
                cur.execute("PRAGMA foreign_keys=ON;")
            except Exception as e:
                logger.warning("Could not enable WAL for SQLite (filesystem may not support it): %s. Continuing with default journal.", e)
                try:
                    cur.execute("PRAGMA foreign_keys=ON;")
                except Exception:
                    pass
            finally:
                try:
                    cur.close()
                except Exception:
                    pass
        except Exception as ee:
            logger.exception("Error setting SQLite pragmas: %s", ee)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


def init_db() -> None:
    # Import models so SQLAlchemy registers metadata
    from app import models  # noqa: F401
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
