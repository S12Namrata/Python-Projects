from flask import Flask
from flask import render_template, request
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from imdb_web_scrap import *



app = Flask(__name__)

database_file = "sqlite:///movies.db"

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
class Movie(db.Model):
    names = db.Column(db.String(80), primary_key=True)
    links = db.Column(db.String(1024))
    image_links = db.Column(db.String(1024))
    def __repr__(self):
        return "<Names : {}>".format(self.names) 
db. create_all()

@app.route('/search', methods=['GET','POST'])
def search():
    """Renders the html page to search"""
    return render_template("search.html")

@app.route('/find', methods=['GET','POST'])
def find():
    """Finds and returns the movie by movie name"""
    if request.method == 'POST':
        if request.form :
            movie_names=request.form.get('search_movie')
            movie = Movie.query.filter_by(names=movie_names).first()
            db.session.commit() 
    return render_template("search.html", movie=movie)

@app.route('/edit', methods=['GET','POST'])
def edit():
    """Renders the html page to update the selected movie name"""
    if request.method == 'POST':
            if request.form :
                movie_name=request.form.get('movie_name') 
                return render_template("update.html",old_movie=movie_name)
    return render_template("update.html")

@app.route('/update', methods=['GET','POST'])
def update():
    """Updates the movie name and returns list of all movies"""
    if request.method == 'POST':
        if request.form :
            if request.form.get('new_names') and request.form.get('old_names'):
                new_names=request.form.get('new_names')
                old_names=request.form.get('old_names')

                movie = Movie.query.filter_by(names=old_names).first()
                movie.names=new_names
                db.session.add(movie)
                db.session.commit() 
    movies = Movie.query.all()
    return render_template("home.html", movies=movies)


@app.route('/add', methods=['GET','POST'])
def add():
    """Renders the html page to add a new movie to database"""
    return render_template("add.html")

@app.route('/insert', methods=['GET','POST'])
def insert():
    """Inserts the given movie (name, link, image link) and returns list of all movies"""
    if request.method == 'POST':
        if request.form :
            if request.form.get('names') and request.form.get('links') and request.form.get('image_links'):
                movie = Movie(names=request.form.get('names'),
                            links=request.form.get('links'), 
                            image_links=request.form.get('image_links'))
                db.session.add(movie)
                db.session.commit() 
    movies = Movie.query.all()
    return render_template("home.html", movies=movies)


@app.route('/delete', methods=['GET','POST'])
def delete():
    """Deletes the selected movie by name and returns list of all movies"""
    if request.method == 'POST':
            if request.form :
                if request.form.get('movie_name'):
                    movie_name=request.form.get('movie_name')
                    movie = Movie.query.filter_by(names=movie_name).first()
                    db.session.delete(movie)
                    db.session.commit() 
    movies = Movie.query.all()
    return render_template("home.html", movies=movies)

@app.route('/scrap', methods=['GET','POST'])
def scrap():
    """Renders the html page to scrap data from IMDB"""
    return render_template("webscrap.html")

@app.route('/all', methods=['GET','POST'])
def send_all():
    """Renders the html page to display list of all the movies"""
    url="https://www.imdb.com/search/title?genres=drama&groups=top_250&sort=user_rating,desc"
    if request.method == 'POST':
        if request.form :
            if request.form.get('sel1'):
                url=request.form.get('sel1') 
    web_scrap(url)
    movies = populate_from_csv()
    return render_template("home.html", movies=movies)
    
@app.route('/', methods=['GET','POST'])
def default_page():
    url="https://www.imdb.com/search/title?genres=drama&groups=top_250&sort=user_rating,desc"
    web_scrap(url)
    movies = populate_from_csv()
    return render_template("home.html", movies=movies)

def populate_from_csv():
    """Reads and populates movie data from csv into databse, and Renders the html page to display list of all the movies"""
    df = pd.read_csv("imdb1.csv", sep=",")   
    for row in df.iterrows():
            movie_db = Movie.query.filter_by(names=row[1]['names']).first()
            if not movie_db:
                movie = Movie(names=row[1]['names'],
                            links=row[1]['links'], 
                            image_links=row[1]['image_links'])
                db.session.add(movie)
                db.session.commit()         
    movies = Movie.query.all()
    return movies

def web_scrap(url):
    scrap_IMDB_page(url)

if __name__ == '__main__':
    app.run()
