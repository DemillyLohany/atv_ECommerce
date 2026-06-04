from models.models import Enderecos
from database.database import get_session
from typing import Annotated, TypeAlias
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session
from routes.login_router import UsuarioLogado

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/enderecos",
    tags=["enderecos"]
)

@router.get("/", response_model=list[Enderecos])
def get_enderecos(
    usuario: UsuarioLogado,
    session: SessionDep
) -> list[Enderecos]:
    return session.query(Enderecos).all()

@router.get("/{id}", response_model=Enderecos)
def get_endereco_by_id(
    id: int,
    usuario: UsuarioLogado,
    session: SessionDep
) -> Enderecos:
    endereco = session.query(Enderecos).get(id)

    if not endereco:
        raise HTTPException(
            status_code=404,
            detail="Endereço não encontrado"
        )

    return endereco

@router.post("/", response_model=Enderecos)
def create_endereco(
    endereco: Enderecos,
    usuario: UsuarioLogado,
    session: SessionDep
) -> Enderecos:
    session.add(endereco)
    session.commit()
    session.refresh(endereco)

    return endereco

@router.delete("/{id}")
def delete_endereco(
    id: int,
    usuario: UsuarioLogado,
    session: SessionDep
):
    endereco = session.query(Enderecos).get(id)

    if not endereco:
        raise HTTPException(
            status_code=404,
            detail="Endereço não encontrado"
        )

    session.delete(endereco)
    session.commit()

    return {"mensagem": "Endereço removido com sucesso"}

@router.put("/{id}")
def update_endereco(
    id: int,
    endereco: Enderecos,
    usuario: UsuarioLogado,
    session: SessionDep
):
    endereco_db = session.query(Enderecos).get(id)

    if not endereco_db:
        raise HTTPException(
            status_code=404,
            detail="Endereço não encontrado"
        )

    session.query(Enderecos).filter(
        Enderecos.id == id
    ).update(
        endereco.model_dump(exclude={"id"})
    )

    session.commit()

    return {"mensagem": "Endereço atualizado com sucesso"}