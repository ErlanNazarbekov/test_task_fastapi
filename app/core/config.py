from typing import Optional
from pydantic import EmailStr, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str
    database_url: str
    secret: str
    first_superuser_email: Optional[EmailStr]
    first_superuser_password: Optional[str]

    model_config = ConfigDict(env_file='.env')


settings = Settings()
