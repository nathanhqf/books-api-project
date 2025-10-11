"""
Modelos Pydantic para Autenticação
"""

from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(..., description="Nome de usuário")
    password: str = Field(..., description="Senha")

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Token de acesso JWT")
    refresh_token: str = Field(..., description="Token de refresh JWT")
    token_type: str = Field(default="bearer", description="Tipo do token")

class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., description="Token de refresh")
