from pathlib import Path


def ensure_data_dir() -> None:
    Path("./data").mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    ensure_data_dir()
    from app.db.session import engine
    from app.db import models
    models.Base.metadata.create_all(bind=engine)
    print('Initialized DB')
