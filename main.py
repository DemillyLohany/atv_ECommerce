from fastapi import FastAPI
from routes import usuario_routes,papel_router,login_router

app = FastAPI()
app.include_router(usuario_routes.router)
app.include_router(papel_router.router)
app.include_router(login_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

#iniciar banco de dados:
#.\mysqld --initialize-insecure --console

#ativar o servidor: .\mysqld --console
