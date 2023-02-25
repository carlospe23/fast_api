from fastapi import FastAPI
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from fastapi.responses import HTMLResponse, JSONResponse
from routers.movie_router import movie_router
from routers.user_router import user_router


app = FastAPI()
# localhost:8000/docs -> abre documentacion autogenerada
# y los parametros de abajo son los editables
app.title = 'Mi aplicacion con FastAPI'
app.version = '0.0.1'

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)


Base.metadata.create_all(bind=engine)


# para iniciar el servidor usamos: 
# uvicorn main:app --reload --port 3000  [--host 0.0.0.0 lo abre para que sea disponible en toda la red local]
@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')
