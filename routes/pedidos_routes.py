from models.models import Pedidos
from database.database import get_session
from typing import Annotated, TypeAlias
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.get("/", response_model=list[Pedidos])
def get_pedidos(session: SessionDep) -> list[Pedidos]:
    return session.query(Pedidos).all()

@router.get("/{id}", response_model=Pedidos)
def get_pedido_by_id(id: int, session: SessionDep) -> Pedidos:
    pedido = session.query(Pedidos).get(id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@router.post("/", response_model=Pedidos)
def create_pedido(pedido: Pedidos, session: SessionDep) -> Pedidos:
    session.add(pedido)
    session.commit()
    session.refresh(pedido)
    return pedido

@router.delete("/{id}")
def delete_pedido(id: int, session: SessionDep) -> None:
    pedido = session.query(Pedidos).get(id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    session.delete(pedido)
    session.commit()

@router.put("/{id}")
def update_pedido(id: int, pedido: Pedidos, session: SessionDep):
    pedido_db = session.query(Pedidos).get(id)
    if not pedido_db:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    dados_atualizados = {
        getattr(Pedidos, k): v 
        for k, v in pedido.model_dump(exclude_unset=True).items() 
        if hasattr(Pedidos, k)
    }
    
    session.query(Pedidos).filter_by(id=id).update(dados_atualizados)
    session.commit()
    return {"mensagem": "Pedido atualizado com sucesso"}