from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Baynext API"
    root_path: str = "/api"
    ml_api_secret_api_key: SecretStr

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
