from fastapi import FastAPI, Depends, Request, Form
from starlette.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
import schema
from database import SessionLocal, engine
import model
from fastapi.encoders import jsonable_encoder

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


model.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get('/')
def root():
    return {"message": "Welcome to simple fastapi app"}



@app.get('/movie/', response_class=HTMLResponse)
async def read_movies(request: Request, db: Session = Depends(get_database_session)):
    records = db.query(model.Movie).all()
    return templates.TemplateResponse("index.html", {"request": request, "data": records})


@app.get("/movie/{name}", response_class=HTMLResponse)
def read_movie(request: Request, name: schema.Movie.name, db: Session = Depends(get_database_session)):
    item = db.query(model.Movie).filter(model.Movie.id==name).first()
    print(item)
    return templates.TemplateResponse("overview.html", {"request": request, "movie": item})



@app.post("/movie/")
async def create_movie(db: Session = Depends(get_database_session), name: schema.Movie.name = Form(...), url: schema.Movie.url = Form(...), rate: schema.Movie.rating = Form(...), type: schema.Movie.type = Form(...), desc: schema.Movie.desc = Form(...)):
    movie = model.Movie(name=name, url=url, rating=rate, type=type, desc=desc)
    db.add(movie)
    db.commit()
    response = RedirectResponse('/', status_code=303)
    return response


@app.patch("/movie/{id}")
async def update_movie(request: Request, id: int, db: Session = Depends(get_database_session)):
    requestBody = await request.json()
    movie = db.query(model.Movie).get(id)
    movie.name = requestBody['name']
    movie.desc = requestBody['desc']
    db.commit()
    db.refresh(movie)
    newMovie = jsonable_encoder(movie)
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success",
        "movie": newMovie
    })


@app.delete("/movie/{id}")
async def delete_movie(request: Request, id: int, db: Session = Depends(get_database_session)):
    movie = db.query(model.Movie).get(id)
    db.delete(movie)
    db.commit()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success",
        "movie": None
    })