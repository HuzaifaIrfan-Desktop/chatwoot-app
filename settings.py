
from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    chatwoot_url: str = Field(default="http://chatwoot.home:3000/", json_schema_extra={"env": "chatwoot_url"})
    chatwoot_ws_url: str = Field(default="ws://chatwoot.home:3000/", json_schema_extra={"env": "chatwoot_ws_url"})
    # access_token: str = Field(default="" json_schema_extra={"env": "access_token"})
    inbox_identifier: str = Field(default="", json_schema_extra={"env": "inbox_identifier"})
    contact_identifier: str = Field(default="", json_schema_extra={"env": "contact_identifier"})

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )


  