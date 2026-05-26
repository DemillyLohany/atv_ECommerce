from models.models import Usuarios
from database.database import get_session
from typing import Annotated, TypeAlias
from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/", response_model=list[Usuarios])
def get_usuarios(session: SessionDep) -> list[Usuarios]:
    return session.query(Usuarios).all()

@router.get("/{id}", response_model=Usuarios)
def get_usuario_by_id(id: int, session: SessionDep) -> Usuarios:
    usuario = session.query(Usuarios).get(id)
   
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.post("/", response_model=Usuarios)
def create_usuario(usuario: Usuarios, session: SessionDep) -> Usuarios:
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

@router.delete("/{id}")
def delete_usuario(id: int, session: SessionDep) -> None:
    usuario = session.query(Usuarios).get(id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    session.delete(usuario)
    session.commit()

@router.put("/{id}")
def update_usuario(id: int, usuario: Usuarios, session: SessionDep):
  
    usuario_db = session.query(Usuarios).get(id)
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    dados_atualizados = {
        getattr(Usuarios, k): v for k, v in usuario.model_dump(exclude_unset=True).items() 
        if hasattr(Usuarios, k)}
    
    session.query(Usuarios).filter_by(id=id).update(dados_atualizados)
    session.commit()
    return {"mensagem": "Usuário atualizado com sucesso"}