from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str # str because going to URL anyway (a sequence of characters)
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env" # tells Pydantic to read from .env file, '.env' is the standard name

settings = Settings()