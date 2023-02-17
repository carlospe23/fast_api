from fastapi import FastAPI
from fastapi import Body, Path, Query
from pydantic import BaseModel, Field
from typing import Optional

from fastapi.responses import HTMLResponse

app = FastAPI()
# localhost:8000/docs -> abre documentacion autogenerada
# y los parametros de abajo son los editables
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

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
                'overview': "Descripccion de la pelicula",
                'year': 2022,
                'rating': 9.8,
                'category': 'Acción'
            }
        }


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'
    },

    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'
    },

    {
        'id': 3,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
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


@app.get('/movies', tags=['movies'])
def get_movies():
    return movies


@app.get('/movie/{id}', tags=['movies'])
def get_movie(id: int = Path(ge = 1, le = 2000)):
    movie = list(filter(lambda x: x['id'] == id, movies))
    return movie or 'No hay nada pai'


@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    movies_filter = list(filter(lambda x: x['category'] == category, movies))
    return movies_filter or 'noting pai'


@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies


@app.put('/movie/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie):
            for item in movies:
                if item['id'] == id:
                    item['title'] = movie.title
                    item['overview'] = movie.overview
                    item['year'] = movie.year
                    item['rating'] = movie.rating
                    item['category'] = movie.category

            return movies


@app.delete('/movie/{id}', tags=['movies'])
def delete_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)

    return movies
