from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import usuario_routes, papel_router, login_router, categorias_routes, \
avaliacoes_routes, enderecos_routes, estoque_routes, pagamentos_routes, \
pedidos_routes, produtos_routes

from database.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(usuario_routes.router)
app.include_router(papel_router.router)
app.include_router(login_router.router)
app.include_router(categorias_routes.router)
app.include_router(avaliacoes_routes.router)
app.include_router(enderecos_routes.router)
app.include_router(estoque_routes.router)
app.include_router(pagamentos_routes.router)
app.include_router(pedidos_routes.router)
app.include_router(produtos_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)