from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Baynext API"
    bucket_name: str = "lgrosjean-blob"
    ml_api_secret_api_key: SecretStr
    database_url: SecretStr
    blob_read_write_token: SecretStr

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
