from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    secret_key: str
    mail_username: str = "test"
    mail_password: str = "test"
    mail_from: str = "admin25@web.com"
    mail_port: int = 1025
    mail_server: str ="localhost"

    class Config:
        env_file = ".env"
        extra = 'allow'
settings = Settings()