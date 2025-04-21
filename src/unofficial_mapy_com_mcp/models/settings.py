from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_key: SecretStr

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False, extra='ignore')
