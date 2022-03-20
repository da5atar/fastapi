from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_USER: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRATION_TIME: int

    class Config:
        env_file = ".env"

settings = Settings()