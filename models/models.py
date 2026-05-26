#-------------------------------------------
# Seguindo a parte 1 da atividade ECommerce

from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel,Field

class Usuarios(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str = Field(default=None, nullable=False)
    email: EmailStr = Field(default=None, nullable=False, unique=True)
    senha_hash: str = Field(default=None, nullable=False)
    criado_em: datetime = Field(default_factory=datetime.now)

class Papeis(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str = Field(default=None, nullable=False)

class UsuariosPapeis(SQLModel, table=True):
    id_usuario: int = Field(default=None,primary_key=True, foreign_key="usuario.id")
    id_papel: int = Field(default=None,primary_key=True, foreign_key="papel.id")

class Produtos(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str = Field(default=None, nullable=False)
    preco: float = Field(default=None, nullable=False)
    descricao: str = Field(default=None, nullable=False)
    criado_em: datetime = Field(default_factory=datetime.now)

class Categorias(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str = Field(default=None, nullable=False)

class ProdutosCategorias(SQLModel, table=True):
    id_produto: int = Field(default=None, primary_key=True,foreign_key="produto.id")
    id_categoria: int = Field(default=None, primary_key=True,foreign_key="categoria.id")

class Pedidos(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    id_usuario: int = Field(default=None, foreign_key="usuario.id")
    total: float = Field(default=None, nullable=False)
    status: str = Field(default=None, nullable=False)
    criado_em: datetime = Field(default_factory=datetime.now)

class ItensPedido(SQLModel, table=True):
    id_pedido: int = Field(default=None,primary_key=True, foreign_key="pedido.id")
    id_produto: int = Field(default=None, primary_key=True,foreign_key="produto.id")
    quantidade: int = Field(default=None, nullable=False)
    preco: float = Field(default=None, nullable=False)

class Pagamentos(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    id_pedido: int = Field(default=None, foreign_key="pedido.id")
    valor: float = Field(default=None, nullable=False)
    metodo: str = Field(default=None, nullable=False)
    status: str = Field(default=None, nullable=False)
    pago_em: datetime = Field(default_factory=datetime.now)

class Enderecos(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    id_usuario: int = Field(default=None, foreign_key="usuario.id")
    rua: str = Field(default=None, nullable=False)
    cidade: str = Field(default=None, nullable=False)
    estado: str = Field(default=None, nullable=False)
    cep: str = Field(default=None, nullable=False)

class Avaliacoes(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    id_produto: int = Field(default=None, foreign_key="produto.id")
    id_usuario: int = Field(default=None, foreign_key="usuario.id")
    nota: int = Field(default=None, nullable=False)
    comentario: str = Field(default=None, nullable=False)
    criado_em: datetime = Field(default_factory=datetime.now)

class Estoque(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    id_produto: int = Field(default=None, foreign_key="produto.id")
    quantidade: int = Field(default=None, nullable=False)
    atualizado_em: datetime = Field(default_factory=datetime.now)