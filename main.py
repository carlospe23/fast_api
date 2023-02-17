from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from typing import Optional

from fastapi.responses import HTMLResponse

app = FastAPI()
# localhost:8000/docs -> abre documentacion autogenerada
# y los parametros de abajo son los editables
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

class Movie(BaseModel):
    id: Optional[int] = None
    title: str
    overview: str
    year: int
    rating: float
    category: str

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
def get_movie(id: int):
    movie = list(filter(lambda x: x['id'] == id, movies))
    return movie or 'No hay nada pai'


@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year: int):
    movies_filter = list(filter(lambda x: x['category'] == category or x['year'] == year, movies))
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
