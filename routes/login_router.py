import os
from datetime import datetime, timedelta
from tokenize import Token

from starlette import status

from models.models import Usuarios, Papel
from database.database import Session, get_session
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated
from sqlmodel import select
from pwdlib import PasswordHash
from dotenv import load_dotenv
import jwt

load_dotenv()
senha_context = PasswordHash.recommended()
SessionDep = Annotated[Session,Depends(get_session)]
oauth_schema = OAuth2PasswordBearer(tokenUrl="token")
SECRET = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
router = APIRouter(prefix="/login",tags=["login"])

def validar_senha(senha:str, hash_password:str)->bool:
    return senha_context.verify(password=senha, hash=hash_password)

def create_access_token(data:dict,expires:timedelta=None)-> str:
    to_encode = data.copy()
    if expires:
        expires_date = datetime.now() + expires
    else:
        expires_date = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp":expires_date})
    jwt_encode= jwt.encode(to_encode,SECRET,algorithm=ALGORITHM)
    return jwt_encode

def get_usuario(token:Annotated[str,Depends(oauth_schema)],
                session:SessionDep
                )-> Usuarios:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Usuário/Senha incorreta',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        dados=jwt.decode(token,SECRET,algorithms=[ALGORITHM])
        email = dados['sub']
        if not email:
            raise credentials_exception
        usuario = session.scalar(
            select(Usuarios).where(
                Usuarios.email == email)
        )
        if not usuario:
            raise credentials_exception
        return usuario
    except Exception:
        raise credentials_exception
@router.post("/")
def login(session: SessionDep,
                form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = session.scalar(
        select(Usuarios).where(
            Usuarios.email == form_data.username
        )
    )
    if not usuario:
        raise HTTPException(status_code=401,
                            detail="Usuário/senha incorreta")
    if not validar_senha(form_data.password,
                                       usuario.senha_hash):
        raise HTTPException(status_code=401,
                            detail="Usuário/senha incorreta")

    access_token = create_access_token(data={
        'sub':usuario.email
    })
    return {'access_token':access_token,
            'token_type':'bearer'}

# Crie o atalho de tipo sem o Depends
UsuarioLogado = Annotated[Usuarios, Depends(get_usuario)]

