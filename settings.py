
from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    chatwoot_url: str = Field(default="http://chatwoot.home:3000/", alias="chatwoot_url")
    chatwoot_ws_url: str = Field(default="ws://chatwoot.home:3000/", alias="chatwoot_ws_url")
    # access_token: str = Field(default="" alias="access_token")
    inbox_identifier: str = Field(default="KcqVejEih7hcWaU1rueYjQye", alias="inbox_identifier")
    contact_identifier: str = Field(default="rMrFTmeVB9vMSTqeoPpnnV7d", alias="contact_identifier")

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        populate_by_name=True 
    )


  