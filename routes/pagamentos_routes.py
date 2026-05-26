from models.models import Pagamentos
from database.database import get_session
from typing import Annotated, TypeAlias
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix="/pagamentos", tags=["pagamentos"])

@router.get("/", response_model=list[Pagamentos])
def get_pagamentos(session: SessionDep) -> list[Pagamentos]:
    return session.query(Pagamentos).all()

@router.get("/{id}", response_model=Pagamentos)
def get_pagamento_by_id(id: int, session: SessionDep) -> Pagamentos:
    pagamento = session.query(Pagamentos).get(id)
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return pagamento

@router.post("/", response_model=Pagamentos)
def create_pagamento(pagamento: Pagamentos, session: SessionDep) -> Pagamentos:
    session.add(pagamento)
    session.commit()
    session.refresh(pagamento)
    return pagamento

@router.delete("/{id}")
def delete_pagamento(id: int, session: SessionDep) -> None:
    pagamento = session.query(Pagamentos).get(id)
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    session.delete(pagamento)
    session.commit()

@router.put("/{id}")
def update_pagamento(id: int, pagamento: Pagamentos, session: SessionDep):
    pagamento_db = session.query(Pagamentos).get(id)
    if not pagamento_db:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    
    dados_atualizados = {
        getattr(Pagamentos, k): v 
        for k, v in pagamento.model_dump(exclude_unset=True).items() 
        if hasattr(Pagamentos, k)
    }
    
    session.query(Pagamentos).filter_by(id=id).update(dados_atualizados)
    session.commit()
    return {"mensagem": "Pagamento atualizado com sucesso"}