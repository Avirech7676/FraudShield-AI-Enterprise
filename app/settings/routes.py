from fastapi import APIRouter, Depends
from app.auth.jwt_handler import JWTHandler
from .service import (
    get_user_settings,
    get_system,
    get_health,
    reload_models,
    clear_cache,
    restart_engine
)

router = APIRouter(
    prefix="/settings",
    tags=["Settings"]
)

@router.get("")
def settings(user=Depends(JWTHandler.verify_token)):
    return get_user_settings(user)

@router.get("/system")
def system():
    return get_system()

@router.get("/health")
def health():
    return get_health()

@router.post("/reload-model")
def reload():
    return reload_models()

@router.post("/clear-cache")
def clear():
    return clear_cache()

@router.post("/restart-engine")
def restart():
    return restart_engine()