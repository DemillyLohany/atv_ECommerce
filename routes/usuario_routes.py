from models.models import Usuarios
from database.database import get_session
from typing import Annotated
from fastapi import Depends, APIRouter
from pwdlib import PasswordHash

SessionDep = Annotated[get_session, Depends(get_session)]
router = APIRouter(prefix="/usuarios", tags=["usuarios"])
#Criar o contexto de geração de hash - Argon2
senha_context = PasswordHash.recommended()

@router.get("/", response_model=list[Usuarios])
def get_usuarios(session: SessionDep)->list[Usuarios]:
    return session.query(Usuarios).all()

@router.get("/{id}", response_model=Usuarios)
def get_usuario_by_id(id: int, session: SessionDep)->Usuarios:
    return session.query(Usuarios).get(id)

@router.post("/", response_model=Usuarios)
def create_usuario(usuario: Usuarios, session: SessionDep)-> Usuarios:
    usuario.senha_hash = senha_context.hash(usuario.senha_hash)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

@router.delete("/{id}")
def delete_usuario(id: int, session: SessionDep)-> None:
    usuario = session.query(Usuarios).get(id)
    session.delete(usuario)
    session.commit()

@router.put("/{id}")
def update_usuario(id: int, usuario: Usuarios, session: SessionDep):
    session.query(Usuarios).filter(Usuarios.id == id).update(usuario.model_dump())