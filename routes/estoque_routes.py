from models.models import Estoque
from database.database import get_session
from typing import Annotated, TypeAlias
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session
from routes.login_router import UsuarioLogado

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/estoque",
    tags=["estoque"]
)

@router.get("/", response_model=list[Estoque])
def get_estoque(
    usuario: UsuarioLogado,
    session: SessionDep
) -> list[Estoque]:
    return session.query(Estoque).all()

@router.get("/{id}", response_model=Estoque)
def get_estoque_by_id(
    id: int,
    usuario: UsuarioLogado,
    session: SessionDep
) -> Estoque:
    estoque = session.query(Estoque).get(id)

    if not estoque:
        raise HTTPException(
            status_code=404,
            detail="Estoque não encontrado"
        )

    return estoque

@router.post("/", response_model=Estoque)
def create_estoque(
    estoque: Estoque,
    usuario: UsuarioLogado,
    session: SessionDep
) -> Estoque:
    session.add(estoque)
    session.commit()
    session.refresh(estoque)

    return estoque

@router.delete("/{id}")
def delete_estoque(
    id: int,
    usuario: UsuarioLogado,
    session: SessionDep
):
    estoque = session.query(Estoque).get(id)

    if not estoque:
        raise HTTPException(
            status_code=404,
            detail="Estoque não encontrado"
        )

    session.delete(estoque)
    session.commit()

    return {"mensagem": "Estoque removido com sucesso"}

@router.put("/{id}")
def update_estoque(
    id: int,
    estoque: Estoque,
    usuario: UsuarioLogado,
    session: SessionDep
):
    estoque_db = session.query(Estoque).get(id)

    if not estoque_db:
        raise HTTPException(
            status_code=404,
            detail="Estoque não encontrado"
        )

    session.query(Estoque).filter(
        Estoque.id == id
    ).update(
        estoque.model_dump(exclude={"id"})
    )

    session.commit()

    return {"mensagem": "Estoque atualizado com sucesso"}