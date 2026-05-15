from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str

    MONGO_URI: str
    DATABASE_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    OLLAMA_MODEL: str
    EMBEDDING_MODEL: str

    class Config:
        env_file = ".env"


settings = Settings()