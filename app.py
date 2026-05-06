# Pesquisar: Uso da biblioteca request

#-------------------------------------------
# Seguindo a parte 2 da atividade ECommerce
#-------------------------------------------

from database import create_db, get_session
from fastapi import FastAPI, Depends, Form, HTTPException
from typing import Annotated
from sqlmodel import Session
from contextlib import asynccontextmanager
from sqlmodel import select
from model import Usuarios, Produtos, Tarefa, Categorias, \
Pedidos, Pagamentos, Enderecos, Avaliacoes, Estoque

SessionDep = Annotated[Session,Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db() 
    yield

app = FastAPI(lifespan=lifespan)

# -----------------------
# CRUD das tarefas
# -----------------------

@app.get("/tarefas")
def listar_tarefas(session: SessionDep) -> list[Tarefa]:
    lista = session.exec(select(Tarefa)).all() 
    return list(lista)

@app.post('/tarefas')
def cadastrar_tarefas(tarefa:Tarefa, session:SessionDep) -> Tarefa:
    session.add(tarefa)
    session.commit()
    session.refresh(tarefa)
    return tarefa

@app.put("/tarefas/{id}")
def atualizar_tarefas(id:int, tarefa:Tarefa,
session:SessionDep) -> Tarefa:
    tarefaUpdate = session.get(Tarefa,id)
    if tarefaUpdate is None:
        raise HTTPException(404, "Tarefa não encontrada")
    tarefaUpdate.descricao = tarefa.descricao
    tarefaUpdate.nome = tarefa.nome
    tarefaUpdate.status = tarefa.status
    session.add(tarefaUpdate)
    session.commit()
    session.refresh(tarefaUpdate)
    return tarefaUpdate

@app.delete('/tarefas/{id}')
def deletar_tarefas (id:int, session:SessionDep):
    tarefa = session.get(Tarefa, id)
    if tarefa is None:
        raise HTTPException(404, "Tarefa não encontrada")
    session.delete(tarefa)
    session.commit()

# -----------------------
# CRUD dos usuários
# -----------------------

@app.get("/usuarios")
def listar_usu(session: SessionDep) -> list[Usuarios]:
    lista = session.exec(select(Usuarios)).all() 
    return list(lista)

@app.post('/usuarios')
def cadastrar_usu(usuario: Usuarios, session:SessionDep ) -> Usuarios:
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

@app.put('/usuarios/{id}')
def atualizar_usu(id:int, usuario:Usuarios,
session:SessionDep) -> Usuarios:
    usuarioUpdate = session.get(Usuarios, id)

    if usuarioUpdate is None:
        raise HTTPException(404, "Usuario não encontrado")
    
    usuarioUpdate.email = usuario.email
    usuarioUpdate.nome = usuario.nome
    usuarioUpdate.senha_hash  = usuario.senha_hash

    session.add(usuarioUpdate)
    session.commit()
    session.refresh(usuarioUpdate)

    return usuarioUpdate

@app.delete('/usuarios/{id}')
def deletar_usu(id:int, session:SessionDep):
    usuario = session.get(Usuarios, id)
    if usuario is None:
        raise HTTPException(404, "Usuario não encontrado")
    session.delete(usuario)
    session.commit()

# -----------------------
# CRUD dos produtos
# -----------------------

@app.get("/produtos")
def listar_produtos(session: SessionDep) -> list[Produtos]:
    lista = session.exec(select(Produtos)).all() 
    return list(lista)

@app.post('/produtos')
def cadastrar_produtos(produto: Produtos, session:SessionDep ) -> Produtos:
    session.add(produto)
    session.commit()
    session.refresh(produto)
    return produto

@app.put('/produtos/{id}')
def atualizar_produtos(id:int, produto:Produtos,
session:SessionDep) -> Produtos:
    produtoUpdate = session.get(Produtos, id)
    if produtoUpdate is None:
        raise HTTPException(404, "Produto não encontrado")
         
    produtoUpdate.nome = produto.nome
    produtoUpdate.descricao = produto.descricao
    produtoUpdate.preco  = produto.preco 

    session.add(produtoUpdate)
    session.commit()
    session.refresh(produtoUpdate)

    return produtoUpdate

@app.delete('/produtos/{id}')
def deletar_produtos(id:int, session:SessionDep):
    produto = session.get(Produtos, id)
    if produto is None:
        raise HTTPException(404, "Produto não encontrado")
    session.delete(produto)
    session.commit()

# -----------------------
# CRUD das categorias
# -----------------------

@app.get("/categorias")
def listar_categorias(session: SessionDep) -> list[Categorias]:
    lista = session.exec(select(Categorias)).all() 
    return list(lista)

@app.post('/categorias')
def cadastrar_categorias(categoria: Categorias, session:SessionDep ) -> Categorias:
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

@app.put('/categorias/{id}')
def atualizar_categorias(id:int, categoria:Categorias,
session:SessionDep) -> Categorias:
    categoriaUpdate = session.get(Categorias, id)
    if categoriaUpdate is None:
        raise HTTPException(404, "Categoria não encontrada")
         
    categoriaUpdate.nome = categoria.nome
    session.add(categoriaUpdate)
    session.commit()
    session.refresh(categoriaUpdate)

    return categoriaUpdate

@app.delete('/categorias/{id}')
def deletar_categorias(id:int, session:SessionDep):
    categoria = session.get(Categorias, id)
    if categoria is None:
        raise HTTPException(404, "Categoria não encontrada")
    session.delete(categoria)
    session.commit()

# -----------------------
# CRUD das pedidos
# -----------------------

@app.get("/pedidos")
def listar_pedidos(session: SessionDep) -> list[Pedidos]:
    lista = session.exec(select(Pedidos)).all() 
    return list(lista) 

@app.post('/pedidos')
def cadastrar_pedidos(pedido: Pedidos, session:SessionDep ) -> Pedidos:
    session.add(pedido)
    session.commit()
    session.refresh(pedido)
    return pedido

@app.put('/pedidos/{id}')
def atualizar_pedidos(id:int, pedido:Pedidos,
session:SessionDep) -> Pedidos:
    pedidoUpdate= session.get(Pedidos, id)
    
    if pedidoUpdate is None:
        raise HTTPException(404, "Pedido não encontrado")
        
    pedidoUpdate.usuario_id = pedido.usuario_id
    pedidoUpdate.total = pedido.total
    pedidoUpdate.status = pedido.status
    session.add(pedidoUpdate)
    session.commit()
    session.refresh(pedidoUpdate)

    return pedidoUpdate

@app.delete('/pedidos/{id}')
def deletar_pedidos(id:int, session:SessionDep):
    pedido = session.get(Pedidos, id)
    if pedido is None:
        raise HTTPException(404, "Pedido não encontrado")
    session.delete(pedido)
    session.commit()

# -----------------------
# CRUD dos pagamentos
# -----------------------

@app.get("/pagamentos")
def listar_pagamentos(session: SessionDep) -> list[Pagamentos]:
    lista = session.exec(select(Pagamentos)).all() 
    return list(lista)

@app.post('/pagamentos')
def cadastrar_pagamentos(pagamento: Pagamentos, session:SessionDep ) -> Pagamentos:
    session.add(pagamento)
    session.commit()
    session.refresh(pagamento)
    return pagamento

@app.put('/pagamentos/{id}')
def atualizar_pagamentos(id:int, pagamento:Pagamentos,
session:SessionDep) -> Pagamentos:
    pagamentoUpdate = session.get(Pagamentos, id)
    if pagamentoUpdate is None:
        raise HTTPException(404, "Pagamento não encontrado")
   
    pagamentoUpdate.pedido_id = pagamento.pedido_id
    pagamentoUpdate.valor = pagamento.valor
    pagamentoUpdate.metodo = pagamento.metodo
    pagamentoUpdate.status = pagamento.status
    session.add(pagamentoUpdate)
    session.commit()
    session.refresh(pagamentoUpdate)

    return pagamentoUpdate

@app.delete('/pagamentos/{id}')
def deletar_pagamentos(id:int, session:SessionDep):
    pagamento = session.get(Pagamentos, id)
    if pagamento is None:
        raise HTTPException(404, "Pagamento não encontrado")
    session.delete(pagamento)
    session.commit()

# -----------------------
# CRUD dos enderecos
# -----------------------

@app.get("/enderecos")
def listar_enderecos(session: SessionDep) -> list[Enderecos]:
    lista = session.exec(select(Enderecos)).all() 
    return list(lista)

@app.post('/enderecos')
def cadastrar_enderecos(endereco: Enderecos, session:SessionDep ) -> Enderecos:
    session.add(endereco)
    session.commit()
    session.refresh(endereco)
    return endereco

@app.put('/enderecos/{id}')
def atualizar_enderecos(id:int, endereco:Enderecos,
session:SessionDep) -> Enderecos:
    enderecoUpdate = session.get(Enderecos, id)
    if enderecoUpdate is None:
        raise HTTPException(404, "Endereço não encontrado")

    enderecoUpdate.rua = endereco.rua
    enderecoUpdate.cidade = endereco.cidade
    enderecoUpdate.estado = endereco.estado
    enderecoUpdate.cep = endereco.cep
    enderecoUpdate.usuario_id = endereco.usuario_id
    session.add(enderecoUpdate)
    session.commit()
    session.refresh(enderecoUpdate)

    return enderecoUpdate

@app.delete('/enderecos/{id}')
def deletar_enderecos(id:int, session:SessionDep):
    endereco = session.get(Enderecos, id)
    if endereco is None:
        raise HTTPException(404, "Endereço não encontrado")
    session.delete(endereco)
    session.commit()

# -----------------------
# CRUD das avaliações
# -----------------------

@app.get("/avaliacoes")
def listar_avaliacoes(session: SessionDep) -> list[Avaliacoes]:
    lista = session.exec(select(Avaliacoes)).all() 
    return list(lista)

@app.post('/avaliacoes')
def cadastrar_avaliacoes(avaliacao: Avaliacoes, session:SessionDep ) -> Avaliacoes:
    session.add(avaliacao)
    session.commit()
    session.refresh(avaliacao)
    return avaliacao

@app.put('/avaliacoes/{id}')
def atualizar_avaliacoes(id:int, avaliacao:Avaliacoes,
session:SessionDep) -> Avaliacoes:
    avaliacaoUpdate = session.get(Avaliacoes, id)
    if avaliacaoUpdate is None:
        raise HTTPException(404, "Avaliação não encontrada")
   
    avaliacaoUpdate.usuario_id = avaliacao.usuario_id
    avaliacaoUpdate.produto_id = avaliacao.produto_id
    avaliacaoUpdate.nota = avaliacao.nota
    avaliacaoUpdate.comentario = avaliacao.comentario

    session.add(avaliacaoUpdate)
    session.commit()
    session.refresh(avaliacaoUpdate)

    return avaliacaoUpdate

@app.delete('/avaliacoes/{id}')
def deletar_avaliacoes(id:int, session:SessionDep):
    avaliacao = session.get(Avaliacoes, id)
    if avaliacao is None:
        raise HTTPException(404, "Avaliação não encontrada")
    session.delete(avaliacao)
    session.commit()

# -----------------------
# CRUD do estoque
# -----------------------

@app.get("/estoque")
def listar_estoque(session: SessionDep) -> list[Estoque]:
    lista = session.exec(select(Estoque)).all() 
    return list(lista)

@app.post('/estoque')
def cadastrar_estoque(estoque: Estoque, session:SessionDep ) -> Estoque:
    session.add(estoque)
    session.commit()
    session.refresh(estoque)
    return estoque

@app.put('/estoque/{id}')
def atualizar_estoque(id:int, estoque:Estoque,
session:SessionDep) -> Estoque:
    estoqueUpdate = session.get(Estoque, id)
    if estoqueUpdate is None:
        raise HTTPException(404, "Estoque não encontrado")
   
    estoqueUpdate.produto_id = estoque.produto_id
    estoqueUpdate.quantidade = estoque.quantidade

    session.add(estoqueUpdate)
    session.commit()
    session.refresh(estoqueUpdate)

    return estoqueUpdate

@app.delete('/estoque/{id}')
def deletar_estoque(id:int, session:SessionDep):
    estoque = session.get(Estoque, id)
    if estoque is None:
        raise HTTPException(404, "Estoque não encontrado")
    session.delete(estoque)
    session.commit()
