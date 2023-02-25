from fastapi import APIRouter
from fastapi import Path, Query, Depends
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from fastapi.responses import JSONResponse
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code = 200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get('/movie/{id}', tags=['movies'], response_model=Movie, status_code = 200)
def get_movie(id: int = Path(ge = 1, le = 2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    


@movie_router.get('/movies/', tags=['movies'],  response_model=List[Movie] , status_code = 200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_category(category)
    if result:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    return JSONResponse(status_code=404, content={'message':'Not found'})


@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code = 201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={'message':'Movie added succesfully'})


@movie_router.put('/movie/{id}', tags=['movies'], response_model=dict, status_code = 200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message':'Not found'})

    MovieService(db).update_movie(id, movie)

    return JSONResponse(status_code=200, content={'message':'Movie edited succesfully'})


@movie_router.delete('/movie/{id}', tags=['movies'], response_model=dict, status_code = 200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message':'Not found'})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={'message':'Movie deleted succesfully'})
