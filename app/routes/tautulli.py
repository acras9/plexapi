from fastapi import APIRouter, Header, HTTPException
from services.tautulli_api import TautulliAPI
from core.config import settings

router = APIRouter(
    prefix="/api/tautulli",
    tags=["tautulli"]
)

tautulli_api = TautulliAPI()

async def verify_token(token: str = Header(None)):
    if not token or token != settings.TAUTULLI_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

@router.get("/monthly_usage")
async def read_tautulli_monthly(token: str = Header(None)):
    """월간 Tautulli 사용량 조회"""
    await verify_token(token)
    return tautulli_api.get_monthly_usage()

@router.get("/daily_usage")
async def read_tautulli_daily(token: str = Header(None)):
    """일간 Tautulli 사용량 조회"""
    await verify_token(token)
    return tautulli_api.get_daily_usage()

@router.get("/userstats")
async def read_tautulli_stats(
    period: int,
    region: str,
    token: str = Header(None)
):
    """Tautulli 사용자 통계 조회"""
    await verify_token(token)
    return tautulli_api.get_user_stats(period, region)
