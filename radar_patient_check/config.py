from typing import List, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    server: Optional[str] = None
    with_tunnel: bool = False
    via_app: bool = False

    radar_apikeys: List[str] = []
    ukrdc_apikeys: List[str] = []

    class Config:
        env_file = ".env"


settings = Settings()
