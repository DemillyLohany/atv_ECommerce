from models.models import Usuarios, UsuarioCreate
from database.database import get_session
from typing import Annotated, TypeAlias
from fastapi import Depends, APIRouter, HTTPException
from pwdlib import PasswordHash
from sqlmodel import Session
from routes.login_router import UsuarioLogado

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

senha_context = PasswordHash.recommended()

@router.get("/", response_model=list[Usuarios])
def get_usuarios(
    usuario_logado: UsuarioLogado,
    session: SessionDep
) -> list[Usuarios]:
    return session.query(Usuarios).all()

@router.get("/{id}", response_model=Usuarios)
def get_usuario_by_id(
    id: int,
    usuario_logado: UsuarioLogado,
    session: SessionDep
) -> Usuarios:
    usuario = session.query(Usuarios).get(id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario

@router.post("/", response_model=Usuarios)
def create_usuario(
    usuario: UsuarioCreate,
    session: SessionDep
) -> Usuarios:

    novo_usuario = Usuarios(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_context.hash(usuario.senha_hash)
    )

    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)

    return novo_usuario

@router.delete("/{id}")
def delete_usuario(
    id: int,
    usuario_logado: UsuarioLogado,
    session: SessionDep
):
    usuario = session.query(Usuarios).get(id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    session.delete(usuario)
    session.commit()

    return {"mensagem": "Usuário removido com sucesso"}

@router.put("/{id}")
def update_usuario(
    id: int,
    usuario: Usuarios,
    usuario_logado: UsuarioLogado,
    session: SessionDep
):
    usuario_db = session.query(Usuarios).get(id)

    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    usuario_db.nome = usuario.nome
    usuario_db.email = usuario.email
    usuario_db.senha_hash = senha_context.hash(
        usuario.senha_hash
    )

    session.add(usuario_db)
    session.commit()
    session.refresh(usuario_db)

    return {"mensagem": "Usuário atualizado com sucesso"}