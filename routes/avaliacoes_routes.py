from models.models import Avaliacoes
from database.database import get_session
from typing import Annotated, TypeAlias
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session
from routes.login_router import UsuarioLogado

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/avaliacoes",
    tags=["avaliacoes"]
)

@router.get("/", response_model=list[Avaliacoes])
def get_avaliacoes(
    usuario: UsuarioLogado,
    session: SessionDep
) -> list[Avaliacoes]:
    return session.query(Avaliacoes).all()

@router.get("/{id}", response_model=Avaliacoes)
def get_avaliacao_by_id(
    id: int,
    usuario: UsuarioLogado,
    session: SessionDep
) -> Avaliacoes:
    avaliacao = session.query(Avaliacoes).get(id)

    if not avaliacao:
        raise HTTPException(
            status_code=404,
            detail="Avaliação não encontrada"
        )

    return avaliacao

@router.post("/", response_model=Avaliacoes)
def create_avaliacao(
    avaliacao: Avaliacoes,
    usuario: UsuarioLogado,
    session: SessionDep
) -> Avaliacoes:
    session.add(avaliacao)
    session.commit()
    session.refresh(avaliacao)

    return avaliacao

@router.delete("/{id}")
def delete_avaliacao(
    id: int,
    usuario: UsuarioLogado,
    session: SessionDep
):
    avaliacao = session.query(Avaliacoes).get(id)

    if not avaliacao:
        raise HTTPException(
            status_code=404,
            detail="Avaliação não encontrada"
        )

    session.delete(avaliacao)
    session.commit()

    return {"mensagem": "Avaliação removida com sucesso"}

@router.put("/{id}")
def update_avaliacao(
    id: int,
    avaliacao: Avaliacoes,
    usuario: UsuarioLogado,
    session: SessionDep
):
    avaliacao_db = session.query(Avaliacoes).get(id)

    if not avaliacao_db:
        raise HTTPException(
            status_code=404,
            detail="Avaliação não encontrada"
        )

    session.query(Avaliacoes).filter(
        Avaliacoes.id == id
    ).update(
        avaliacao.model_dump(exclude={"id"})
    )

    session.commit()

    return {"mensagem": "Avaliação atualizada com sucesso"}