from starlette import status
from models.models import Papel
from database.database import get_session, Session
from typing import Annotated, TypeAlias
from fastapi import Depends, APIRouter, HTTPException
from routes.login_router import UsuarioLogado
from sqlmodel import select

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/papeis",
    tags=["papel"]
)

@router.get("/", response_model=list[Papel])
def get_papel(
    usuario: UsuarioLogado,
    session: SessionDep
) -> list[Papel]:
    return session.exec(select(Papel)).all()

@router.get("/{id}", response_model=Papel)
def get_papel_by_id(
    id: int,
    usuario: UsuarioLogado,
    session: SessionDep
) -> Papel:
    papel = session.get(Papel, id)

    if papel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Papel não encontrado"
        )

    return papel

@router.post("/", response_model=Papel)
def create_papel(
    papel: Papel,
    usuario: UsuarioLogado,
    session: SessionDep
) -> Papel:
    session.add(papel)
    session.commit()
    session.refresh(papel)

    return papel

@router.delete("/{id}")
def delete_papel(
    id: int,
    usuario: UsuarioLogado,
    session: SessionDep
):
    papel = session.get(Papel, id)

    if papel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Papel não encontrado"
        )

    session.delete(papel)
    session.commit()

    return {"mensagem": "Papel removido com sucesso"}

@router.put("/{id}", response_model=Papel)
def update_papel(
    id: int,
    papel: Papel,
    usuario: UsuarioLogado,
    session: SessionDep
) -> Papel:
    papel_db = session.get(Papel, id)

    if papel_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Papel não encontrado"
        )

    for key, value in papel.model_dump(
        exclude_unset=True,
        exclude={"id"}
    ).items():
        setattr(papel_db, key, value)

    session.add(papel_db)
    session.commit()
    session.refresh(papel_db)

    return papel_db