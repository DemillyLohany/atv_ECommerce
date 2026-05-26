from models.models import Avaliacoes
from database.database import get_session
from typing import Annotated, TypeAlias
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix="/avaliacoes", tags=["avaliacoes"])

@router.get("/", response_model=list[Avaliacoes])
def get_avaliacoes(session: SessionDep) -> list[Avaliacoes]:
    return session.query(Avaliacoes).all()

@router.get("/{id}", response_model=Avaliacoes)
def get_avaliacao_by_id(id: int, session: SessionDep) -> Avaliacoes:
    avaliacao = session.query(Avaliacoes).get(id)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return avaliacao

@router.post("/", response_model=Avaliacoes)
def create_avaliacao(avaliacao: Avaliacoes, session: SessionDep) -> Avaliacoes:
    session.add(avaliacao)
    session.commit()
    session.refresh(avaliacao)
    return avaliacao

@router.delete("/{id}")
def delete_avaliacao(id: int, session: SessionDep) -> None:
    avaliacao = session.query(Avaliacoes).get(id)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    session.delete(avaliacao)
    session.commit()

@router.put("/{id}")
def update_avaliacao(id: int, avaliacao: Avaliacoes, session: SessionDep):
    avaliacao_db = session.query(Avaliacoes).get(id)
    if not avaliacao_db:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    
    dados_atualizados = {
        getattr(Avaliacoes, k): v 
        for k, v in avaliacao.model_dump(exclude_unset=True).items() 
        if hasattr(Avaliacoes, k)
    }
    
    session.query(Avaliacoes).filter_by(id=id).update(dados_atualizados)
    session.commit()
    return {"mensagem": "Avaliação atualizada com sucesso"}