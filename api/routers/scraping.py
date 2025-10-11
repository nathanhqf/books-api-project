"""
Router de Scraping

Endpoint para disparar o scraping em background (apenas admin).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from api.auth.jwt_handler import get_current_user
import threading
from scripts.scraper import main as run_scraper
from api.config import DATA_PATH
import os

router = APIRouter(prefix="/api/v1/scraping", tags=["Scraping"])


def admin_required(user: dict = Depends(get_current_user)):
    # user é um dict: {"username": ..., ...}
    from api.auth.jwt_handler import FAKE_USERS_DB
    username = user.get("username")
    user_obj = FAKE_USERS_DB.get(username)
    if not user_obj or user_obj.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso permitido apenas para admin.")
    return user_obj

scraping_status = {"running": False, "last_result": None}

def scraping_task():
    scraping_status["running"] = True
    try:
        run_scraper()
        scraping_status["last_result"] = "Scraping concluído com sucesso."
    except Exception as e:
        scraping_status["last_result"] = f"Erro: {str(e)}"
    scraping_status["running"] = False

@router.post("/trigger", summary="Dispara o scraping em background", response_description="Status da operação", status_code=202)
def trigger_scraping(user = Depends(admin_required)):
    if scraping_status["running"]:
        return {"status": "Scraping já está em execução."}
    thread = threading.Thread(target=scraping_task)
    thread.start()
    return {"status": "Scraping iniciado em background."}

@router.get("/status", summary="Consulta status do scraping")
def get_scraping_status(user = Depends(admin_required)):
    return scraping_status
