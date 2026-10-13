from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./data/couponhunter.db"
    ADMIN_TOKEN: str = ""
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    SITE_NAME: str = "CouponHunter MVP"

    class Config:
        env_file = ".env"

settings = Settings()
