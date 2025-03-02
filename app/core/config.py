from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional, List
import os
from dotenv import load_dotenv
from pathlib import Path

# 프로젝트 루트 디렉토리 찾기
PROJECT_ROOT = Path(__file__).parent.parent.parent

load_dotenv()

class Settings(BaseSettings):
    # Tautulli Settings
    TAUTULLI_URL_KOREA: str = Field(..., env='TAUTULLI_URL_KOREA')
    TAUTULLI_KEY_KOREA: str = Field(..., env='TAUTULLI_KEY_KOREA')
    TAUTULLI_URL_GERMAN: str = Field(..., env='TAUTULLI_URL_GERMAN')
    TAUTULLI_KEY_GERMAN: str = Field(..., env='TAUTULLI_KEY_GERMAN')
    TAUTULLI_TOKEN: str = Field(..., env='TAUTULLI_TOKEN')

# 설정 인스턴스 생성 시 명시적으로 env_file 경로 지정
settings = Settings(_env_file=str(PROJECT_ROOT / ".env"))
