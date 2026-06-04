from models.models import Produtos
from database.database import get_session
from typing import Annotated, TypeAlias
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session
from routes.login_router import UsuarioLogado

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/produtos",
    tags=["produtos"]
)

@router.get("/", response_model=list[Produtos])
def get_produtos(
    usuario: UsuarioLogado,
    session: SessionDep
) -> list[Produtos]:
    return session.query(Produtos).all()

@router.get("/{id}", response_model=Produtos)
def get_produto_by_id(
    id: int,
    usuario: UsuarioLogado,
    session: SessionDep
) -> Produtos:
    produto = session.query(Produtos).get(id)

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return produto

@router.post("/", response_model=Produtos)
def create_produto(
    produto: Produtos,
    usuario: UsuarioLogado,
    session: SessionDep
) -> Produtos:
    session.add(produto)
    session.commit()
    session.refresh(produto)
    return produto

@router.delete("/{id}")
def delete_produto(
    id: int,
    usuario: UsuarioLogado,
    session: SessionDep
):
    produto = session.query(Produtos).get(id)

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    session.delete(produto)
    session.commit()

    return {"mensagem": "Produto removido com sucesso"}

@router.put("/{id}")
def update_produto(
    id: int,
    produto: Produtos,
    usuario: UsuarioLogado,
    session: SessionDep
):
    produto_db = session.query(Produtos).get(id)

    if not produto_db:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    session.query(Produtos).filter(
        Produtos.id == id
    ).update(produto.model_dump(exclude={"id"}))

    session.commit()

    return {"mensagem": "Produto atualizado com sucesso"}