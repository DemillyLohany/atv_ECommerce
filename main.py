from fastapi import FastAPI

from routes import (
    usuario_routes,
    produtos_routes,
    pedidos_routes,
    categorias_routes,
    enderecos_routes,
    pagamentos_routes,
    estoque_routes,
    avaliacoes_routes
)

app = FastAPI()

#incluindo todas as rotas da aplicação no servidor
app.include_router(usuario_routes.router) 
app.include_router(produtos_routes.router)
app.include_router(pedidos_routes.router)
app.include_router(categorias_routes.router)
app.include_router(enderecos_routes.router)
app.include_router(pagamentos_routes.router)
app.include_router(estoque_routes.router)
app.include_router(avaliacoes_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)


