"""
Router de Autenticação
"""

from fastapi import APIRouter, HTTPException, status
from api.auth.models import LoginRequest, TokenResponse, RefreshRequest
from api.auth.jwt_handler import authenticate_user, create_access_token, create_refresh_token, decode_token

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticação"])

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """Autentica usuário e retorna tokens JWT"""
    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    
    access_token = create_access_token(data={"sub": user["username"]})
    refresh_token = create_refresh_token(data={"sub": user["username"]})
    
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=TokenResponse)
async def refresh(request: RefreshRequest):
    """Renova o token de acesso usando o refresh token"""
    try:
        payload = decode_token(request.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        
        username = payload.get("sub")
        access_token = create_access_token(data={"sub": username})
        refresh_token = create_refresh_token(data={"sub": username})
        
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
