from models.models import Estoque
from database.database import get_session
from typing import Annotated, TypeAlias
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix="/estoque", tags=["estoque"])

@router.get("/", response_model=list[Estoque])
def get_estoque(session: SessionDep) -> list[Estoque]:
    return session.query(Estoque).all()

@router.get("/{id}", response_model=Estoque)
def get_estoque_by_id(id: int, session: SessionDep) -> Estoque:
    estoque = session.query(Estoque).get(id)
    if not estoque:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    return estoque

@router.post("/", response_model=Estoque)
def create_estoque(estoque: Estoque, session: SessionDep) -> Estoque:
    session.add(estoque)
    session.commit()
    session.refresh(estoque)
    return estoque

@router.delete("/{id}")
def delete_estoque(id: int, session: SessionDep) -> None:
    estoque = session.query(Estoque).get(id)
    if not estoque:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    session.delete(estoque)
    session.commit()

@router.put("/{id}")
def update_estoque(id: int, estoque: Estoque, session: SessionDep):
    estoque_db = session.query(Estoque).get(id)
    if not estoque_db:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    
    dados_atualizados = {
        getattr(Estoque, k): v 
        for k, v in estoque.model_dump(exclude_unset=True).items() 
        if hasattr(Estoque, k)
    }
    
    session.query(Estoque).filter_by(id=id).update(dados_atualizados)
    session.commit()
    return {"mensagem": "Estoque atualizado com sucesso"}