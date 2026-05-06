#-------------------------------------------
# Seguindo a parte 1 da atividade ECommerce
#-------------------------------------------

from sqlmodel import SQLModel, Field, create_engine, Relationship
from datetime import datetime
from decimal import Decimal
from typing import Optional, List


class UsuariosPapeis(SQLModel, table=True):
    __tablename__: str = 'usuarios_papeis'
    usuario_id: int = Field(foreign_key='usuarios.id', primary_key=True)
    papel_id: int = Field(foreign_key='papeis.id', primary_key=True)


class ProdutoCategorias(SQLModel, table=True):
    __tablename__: str = 'produto_categorias'
    produto_id: int = Field(foreign_key='produtos.id', primary_key=True)
    categoria_id: int = Field(foreign_key='categorias.id', primary_key=True)


class Tarefa(SQLModel, table=True):
    __tablename__: str = 'tarefa'
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    status: bool = Field(default=False)


class Usuarios(SQLModel, table=True):
    __tablename__: str = 'usuarios'
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(sa_column_kwargs={"unique": True})
    senha_hash: str
    criado_em: datetime = Field(default_factory=datetime.now)

    pedidos: List["Pedidos"] = Relationship(back_populates="usuario")
    enderecos: List["Enderecos"] = Relationship(back_populates="usuario")
    avaliacoes: List["Avaliacoes"] = Relationship(back_populates="usuario")
    papeis: List["Papeis"] = Relationship(back_populates="usuarios", link_model=UsuariosPapeis)


class Papeis(SQLModel, table=True):
    __tablename__: str = 'papeis'
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(sa_column_kwargs={"unique": True})

    usuarios: List["Usuarios"] = Relationship(back_populates="papeis", link_model=UsuariosPapeis)


class Produtos(SQLModel, table=True):
    __tablename__: str = 'produtos'
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    preco: Decimal = Field(default=0.0, max_digits=10, decimal_places=2)
    criado_em: datetime = Field(default_factory=datetime.now)

    itens_pedido: List["ItensPedido"] = Relationship(back_populates="produto")
    avaliacoes: List["Avaliacoes"] = Relationship(back_populates="produto")
    estoque: Optional["Estoque"] = Relationship(back_populates="produto")
    categorias: List["Categorias"] = Relationship(back_populates="produtos", link_model=ProdutoCategorias)


class Categorias(SQLModel, table=True):
    __tablename__: str = 'categorias'
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str

    produtos: List["Produtos"] = Relationship(back_populates="categorias", link_model=ProdutoCategorias)


class Pedidos(SQLModel, table=True):
    __tablename__: str = 'pedidos'
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key='usuarios.id')
    total: Decimal = Field(default=0.0, max_digits=10, decimal_places=2)
    status: str
    criado_em: datetime = Field(default_factory=datetime.now)

    usuario: Optional["Usuarios"] = Relationship(back_populates="pedidos")
    itens: List["ItensPedido"] = Relationship(back_populates="pedido")
    pagamentos: List["Pagamentos"] = Relationship(back_populates="pedido")


class ItensPedido(SQLModel, table=True):
    __tablename__: str = 'itens_pedido'
    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key='pedidos.id')
    produto_id: int = Field(foreign_key='produtos.id')
    quantidade: int = Field(default=1)
    preco: Decimal = Field(max_digits=10, decimal_places=2)

    pedido: Optional["Pedidos"] = Relationship(back_populates="itens")
    produto: Optional["Produtos"] = Relationship(back_populates="itens_pedido")


class Pagamentos(SQLModel, table=True):
    __tablename__: str = 'pagamentos'
    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key='pedidos.id')
    valor: Decimal = Field(max_digits=10, decimal_places=2)
    metodo: str = Field(max_length=50)
    status: str = Field(max_length=50)
    pago_em: Optional[datetime] = Field(default=None)

    pedido: Optional["Pedidos"] = Relationship(back_populates="pagamentos")


class Enderecos(SQLModel, table=True):
    __tablename__: str = 'enderecos'
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key='usuarios.id')
    rua: str = Field(max_length=150)
    cidade: str = Field(max_length=100)
    estado: str = Field(max_length=100)
    cep: str = Field(max_length=20)

    usuario: Optional["Usuarios"] = Relationship(back_populates="enderecos")


class Avaliacoes(SQLModel, table=True):
    __tablename__: str = 'avaliacoes'
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key='usuarios.id')
    produto_id: int = Field(foreign_key='produtos.id')
    nota: int = Field(ge=0, le=5)
    comentario: str
    criado_em: datetime = Field(default_factory=datetime.now)

    usuario: Optional["Usuarios"] = Relationship(back_populates="avaliacoes")
    produto: Optional["Produtos"] = Relationship(back_populates="avaliacoes")


class Estoque(SQLModel, table=True):
    __tablename__: str = 'estoque'
    id: Optional[int] = Field(default=None, primary_key=True)
    produto_id: int = Field(foreign_key='produtos.id', sa_column_kwargs={"unique": True})
    quantidade: int = Field(default=0)
    atualizado_em: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

    produto: Optional["Produtos"] = Relationship(back_populates="estoque")


engine = create_engine("sqlite:///database.db")


def criar_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    criar_db()
