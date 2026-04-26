from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    secret_key: str

    class Config:
        env_file = ".env"
        extra = 'allow'
settings = Settings()