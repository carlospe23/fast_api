from fastapi import FastAPI
from fastapi import Path, Query, Request, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()
# localhost:8000/docs -> abre documentacion autogenerada
# y los parametros de abajo son los editables
app.title = 'Mi aplicacion con FastAPI'
app.version = '0.0.1'

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth =  await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin':
            raise HTTPException(status_code=403, detail='invalid credentials')


class User(BaseModel):
    email: str
    password: str


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(mins_length=5, max_length=15)
    overview: str = Field(mins_length=5, max_length=50)
    year: int = Field(default=2022 , le=2022)
    rating: float = Field(ge=1 , le=10)
    category: str = Field(min_length=5 , max_length=15)

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'title': 'Mi pelicula',
                'overview': 'Descripccion de la pelicula',
                'year': 2022,
                'rating': 9.8,
                'category': 'Acción'
            }
        }


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': 'En un exuberante planeta llamado Pandora viven...',
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'
    },

    {
        'id': 2,
        'title': 'Avatar',
        'overview': 'En un exuberante planeta llamado Pandora viven...',
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'
    },

    {
        'id': 3,
        'title': 'Avatar',
        'overview': 'En un exuberante planeta llamado Pandora viven...',
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'
    }
]

# para iniciar el servidor usamos: 
# uvicorn main:app --reload --port 3000  [--host 0.0.0.0 lo abre para que sea disponible en toda la red local]
@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')


@app.post('/login', tags=['auth'], status_code = 200)
def login(user: User):
    if user.email == "admin" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code = 200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@app.get('/movie/{id}', tags=['movies'], response_model=Movie, status_code = 200)
def get_movie(id: int = Path(ge = 1, le = 2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    


@app.get('/movies/', tags=['movies'],  response_model=List[Movie] , status_code = 200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).first()
    if result:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    return JSONResponse(status_code=404, content={'message':'Not found'})


@app.post('/movies', tags=['movies'], response_model=dict, status_code = 201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={'message':'Movie added succesfully'})


@app.put('/movie/{id}', tags=['movies'], response_model=dict, status_code = 200)
def update_movie(id: int, movie: Movie) -> dict:
            for item in movies:
                if item['id'] == id:
                    item['title'] = movie.title
                    item['overview'] = movie.overview
                    item['year'] = movie.year
                    item['rating'] = movie.rating
                    item['category'] = movie.category

            return JSONResponse(status_code=200, content={'message':'Movie edited succesfully'})


@app.delete('/movie/{id}', tags=['movies'], response_model=dict, status_code = 200)
def delete_movie(id: int) -> dict:
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)

    return JSONResponse(status_code=200, content={'message':'Movie deleted succesfully'})
