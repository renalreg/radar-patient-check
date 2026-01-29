from typing import List, Optional

from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    SERVER: Optional[str] = None
    WITH_TUNNEL: bool = False
    VIA_APP: bool = False

    RADAR_APIKEYS: List[str] = []
    UKRDC_APIKEYS: List[str] = []

    SQLALCHEMY_DATABASE_URL: str = None

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="allow",
    )


settings = Settings()
