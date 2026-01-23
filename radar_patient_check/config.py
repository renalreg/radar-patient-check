from typing import List, Optional

from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    SERVER: Optional[str] = None
    WITH_TUNNEL: bool = False
    VIA_APP: bool = False

    RADAR_APIKEYS: List[str] = []
    UKRDC_APIKEYS: List[str] = []

    DB_HOST: str = "localhost"
    DATABASE: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_PORT: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="allow",
    )

    @property
    def has_db_credentials(self) -> bool:
        return all(
            [
                self.DB_USER,
                self.DB_PASSWORD,
                self.DB_PORT,
                self.DATABASE,
            ]
        )

    @property
    def database_url(self) -> Optional[str]:
        if not self.has_db_credentials:
            return None
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DATABASE}"
        )


settings = Settings()
