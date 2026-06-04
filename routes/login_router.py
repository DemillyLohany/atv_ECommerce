import os
import uuid
from datetime import datetime, timedelta
from typing import Annotated, TypeAlias

import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select

from models.models import Usuarios
from database.database import Session, get_session
from pwdlib import PasswordHash

load_dotenv()

SECRET = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

if not SECRET or not ALGORITHM:
    raise ValueError("SECRET_KEY ou ALGORITHM não definidos no .env")

senha_context = PasswordHash.recommended()

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/login", tags=["login"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token inválido ou expirado",
    headers={"WWW-Authenticate": "Bearer"},
)

class TokenBlacklist:
    def __init__(self):
        self.tokens = set()

    def add(self, jti: str):
        self.tokens.add(jti)

    def exists(self, jti: str) -> bool:
        return jti in self.tokens


blacklist = TokenBlacklist()

def verificar_senha(senha: str, hash_senha: str) -> bool:
    return senha_context.verify(password=senha, hash=hash_senha)

def criar_token(data: dict, expires: timedelta, tipo: str):
    to_encode = data.copy()

    now = datetime.utcnow()
    exp = now + expires
    jti = str(uuid.uuid4())

    to_encode.update({
        "exp": int(exp.timestamp()),
        "iat": int(now.timestamp()),
        "jti": jti,
        "type": tipo
    })

    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)


def criar_access_token(data: dict):
    return criar_token(data, timedelta(minutes=30), "access")


def criar_refresh_token(data: dict):
    return criar_token(data, timedelta(days=7), "refresh")


def decode_token(token: str):
    return jwt.decode(token, SECRET, algorithms=[ALGORITHM])


def get_usuario(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep
) -> Usuarios:

    try:
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise credentials_exception

        jti = payload.get("jti")

        if blacklist.exists(jti):
            raise credentials_exception

        email = payload.get("sub")

        if not email:
            raise credentials_exception

        user = session.scalar(
            select(Usuarios).where(Usuarios.email == email)
        )

        if not user:
            raise credentials_exception

        return user

    except jwt.ExpiredSignatureError:
        raise credentials_exception

    except jwt.InvalidTokenError:
        raise credentials_exception


UsuarioLogado = Annotated[Usuarios, Depends(get_usuario)]


@router.post("/")
def login(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = session.scalar(
        select(Usuarios).where(Usuarios.email == form_data.username)
    )

    if not user or not verificar_senha(form_data.password, user.senha_hash):
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

    payload = {
        "sub": user.email,
        "role": user.role
    }

    access = criar_access_token(payload)
    refresh = criar_refresh_token(payload)

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh(token: str):

    payload = decode_token(token)

    if payload.get("type") != "refresh":
        raise credentials_exception

    return {
        "access_token": criar_access_token({
            "sub": payload.get("sub"),
            "role": payload.get("role")
        })
    }


@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):

    payload = decode_token(token)

    blacklist.add(payload["jti"])

    return {"msg": "Logout realizado com sucesso"}


@router.get("/me")
def me(user: UsuarioLogado):
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role
    }


def require_role(role_required: str):
    def wrapper(user: UsuarioLogado):
        if user.role != role_required:
            raise HTTPException(status_code=403, detail="Sem permissão")
        return user
    return wrapper


@router.get("/admin")
def admin(user: Usuarios = Depends(require_role("admin"))):
    return {"msg": "Área admin"}