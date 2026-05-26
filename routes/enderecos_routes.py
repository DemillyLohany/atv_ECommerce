from models.models import Enderecos
from database.database import get_session
from typing import Annotated, TypeAlias
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix="/enderecos", tags=["enderecos"])

@router.get("/", response_model=list[Enderecos])
def get_enderecos(session: SessionDep) -> list[Enderecos]:
    return session.query(Enderecos).all()

@router.get("/{id}", response_model=Enderecos)
def get_endereco_by_id(id: int, session: SessionDep) -> Enderecos:
    endereco = session.query(Enderecos).get(id)
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return endereco

@router.post("/", response_model=Enderecos)
def create_endereco(endereco: Enderecos, session: SessionDep) -> Enderecos:
    session.add(endereco)
    session.commit()
    session.refresh(endereco)
    return endereco

@router.delete("/{id}")
def delete_endereco(id: int, session: SessionDep) -> None:
    endereco = session.query(Enderecos).get(id)
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    session.delete(endereco)
    session.commit()

@router.put("/{id}")
def update_endereco(id: int, endereco: Enderecos, session: SessionDep):
    endereco_db = session.query(Enderecos).get(id)
    if not endereco_db:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    
    dados_atualizados = {
        getattr(Enderecos, k): v 
        for k, v in endereco.model_dump(exclude_unset=True).items() 
        if hasattr(Enderecos, k)
    }
    
    session.query(Enderecos).filter_by(id=id).update(dados_atualizados)
    session.commit()
    return {"mensagem": "Endereço atualizado com sucesso"}