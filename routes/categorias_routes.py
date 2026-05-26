from models.models import Categorias
from database.database import get_session
from typing import Annotated, TypeAlias
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix="/categorias", tags=["categorias"])

@router.get("/", response_model=list[Categorias])
def get_categorias(session: SessionDep) -> list[Categorias]:
    return session.query(Categorias).all()

@router.get("/{id}", response_model=Categorias)
def get_categoria_by_id(id: int, session: SessionDep) -> Categorias:
    categoria = session.query(Categorias).get(id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

@router.post("/", response_model=Categorias)
def create_categoria(categoria: Categorias, session: SessionDep) -> Categorias:
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

@router.delete("/{id}")
def delete_categoria(id: int, session: SessionDep) -> None:
    categoria = session.query(Categorias).get(id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    session.delete(categoria)
    session.commit()

@router.put("/{id}")
def update_categoria(id: int, categoria: Categorias, session: SessionDep):
    categoria_db = session.query(Categorias).get(id)
    if not categoria_db:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    dados_atualizados = {
        getattr(Categorias, k): v 
        for k, v in categoria.model_dump(exclude_unset=True).items() 
        if hasattr(Categorias, k)
    }
    
    session.query(Categorias).filter_by(id=id).update(dados_atualizados)
    session.commit()
    return {"mensagem": "Categoria atualizada com sucesso"}