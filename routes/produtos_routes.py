from models.models import Produtos
from database.database import get_session
from typing import Annotated, TypeAlias
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix="/produtos", tags=["produtos"])

@router.get("/", response_model=list[Produtos])
def get_produtos(session: SessionDep) -> list[Produtos]:
    return session.query(Produtos).all()

@router.get("/{id}", response_model=Produtos)
def get_produto_by_id(id: int, session: SessionDep) -> Produtos:
    produto = session.query(Produtos).get(id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/", response_model=Produtos)
def create_produto(produto: Produtos, session: SessionDep) -> Produtos:
    session.add(produto)
    session.commit()
    session.refresh(produto)
    return produto

@router.delete("/{id}")
def delete_produto(id: int, session: SessionDep) -> None:
    produto = session.query(Produtos).get(id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    session.delete(produto)
    session.commit()

@router.put("/{id}")
def update_produto(id: int, produto: Produtos, session: SessionDep):
    produto_db = session.query(Produtos).get(id)
    if not produto_db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    dados_atualizados = {
        getattr(Produtos, k): v 
        for k, v in produto.model_dump(exclude_unset=True).items() 
        if hasattr(Produtos, k)
    }
    
    session.query(Produtos).filter_by(id=id).update(dados_atualizados)
    session.commit()
    return {"mensagem": "Produto updated com sucesso"}