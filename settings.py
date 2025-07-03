
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    chatwoot_url: str = Field(..., env="chatwoot_url")
    access_token: str = Field(..., env="access_token")
    inbox_identifier: str = Field(..., env="inbox_identifier")
    contact_identifier: str = Field(..., env="contact_identifier")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"