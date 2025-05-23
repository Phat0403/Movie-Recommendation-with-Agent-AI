from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str

    GMAIL: str
    GMAIL_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

settings = Settings(_env_file='.env', _env_file_encoding='utf-8')