from flask import Flask, render_template, request,redirect, session, url_for
from database import DatabaseConnect
from uuid import uuid4
from flask_bcrypt import Bcrypt
import requests
import os
from dotenv import load_dotenv

load_dotenv()
dbconnect = DatabaseConnect()
userid = uuid4()

app = Flask("__name__")
app.secret_key="login"
bcrypt = Bcrypt(app)
tmdb_api_key = os.environ.get('API_KEY_TMDB')
# home page
@app.route('/')
def temp():
    return render_template("index.html")

# sign in page
@app.route('/signin', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name",'')
        email = request.form.get("email")
        password = request.form.get("password")
        first_name = name.split()[0] if name else 'Guest'
        # hashing password
        existing_user = dbconnect.Fetch_Password(email)
        if list(existing_user):
            msg = "Email already registered. Please login."
            return render_template("signin.html", msg=msg)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        dbconnect.Insert_user(name,email,hashed_password)
        session['name'] = first_name
        return redirect(url_for('dash'))
    return render_template("signin.html")

# login page
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # validate fields
        if not email or not password:
            msg = "Please enter all fields"
            return render_template('login.html', msg=msg)

        try:
            cursor = dbconnect.Fetch_Password(email)
            cursor_list = list(cursor) # if cursor is empty then it will give error

            # check if user exists
            if not cursor_list:
                msg = "Email not found"
                return render_template('login.html', msg=msg)
            
            user_id = cursor_list[0][0]
            name = cursor_list[0][1]
            hash_password = cursor_list[0][2]
            first_name = name.split()[0] if name else 'Guest'
            # check password
            is_valid = bcrypt.check_password_hash(hash_password, password)

            if is_valid:
                session['email'] = email
                session['name'] = first_name   
                session['user_id'] = user_id  # store name in session too
                return redirect(url_for('dash'))  # redirect instead of render

            else:
                msg = "Invalid password"
                return render_template('login.html', msg=msg)

        except Exception as e:
            print("Error occurred: ", e)
            msg = "Something went wrong. Please try again."
            return render_template('login.html', msg=msg)

    return render_template("login.html")

# logout page redirect to home page
@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/')

# dashboard page
@app.route('/dashboard',methods=["GET", "POST"])
def dash():
    name = session.get('First_name')
    
    return render_template("dashboard.html",name=name)


def insert_data_watchlist(content):
    if request.method == 'POST':
        click_action = request.form.get('action')
        Id = request.form.get('movie_id')
        Type = content
        Title = request.form.get('Title')
        Poster = request.form.get('Poster')
        Rating = request.form.get('Rating')
        dbconnect.insert_movies(Id,Title,Type,Poster,Rating)
        user_id = session.get('user_id')
        if click_action == 'watchlist':
            dbconnect.insert_watchlist(user_id,Id)
# movies pages 
@app.route('/movies',methods=["POST","GET"])
def movies():
    insert_data_watchlist("movie")
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"

    headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {tmdb_api_key}"
    }
    response = requests.get(url, headers=headers)
    films = response.json()
    text = 'Trending Movies'
    placeholder = 'Movies'
    search= "search_movies"
    return render_template("movies.html", films = films,placeholder=placeholder ,text= text,search_bar_fun =search)

@app.route('/single_movies/<movie_id>',methods=["POST","GET"])
def data_about_single(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0NmViNjNiOGI3ZjAyNzQxNzY3YjA0MTk5MmY2NDBlZSIsIm5iZiI6MTc3NzY0MzU1MS41MTcsInN1YiI6IjY5ZjRiMDFmMDUxODdiMWViODIzNzYyNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.WdepCupiGSLB3hLdSje41rfmvWHzE79g8QP7O2zhnq0"
    }

    response = requests.get(url, headers=headers)
    movies = response.json()
    print(movies)
    return render_template("singleMoviePage.html",movies =movies)

@app.route('/search',methods=["GET", "POST"])
def search_movies():
    films = None
    if request.method == "POST":
        if request.form.get('action') == 'watchlist':
            insert_data_watchlist('movie')
            search_term = session.get('search_result')
            if search_term:
                url = "https://api.themoviedb.org/3/search/movie?query={}&include_adult=false&language=en-US&page=1".format(search_term)
                headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {tmdb_api_key}"
                }
                response = requests.get(url, headers=headers)
                films = response.json()
        else:
            session['search_result'] = request.form.get("search_bar")
            search_term = session.get('search_result')
            url = "https://api.themoviedb.org/3/search/movie?query={}&include_adult=false&language=en-US&page=1".format(search_term)
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {tmdb_api_key}"            
                }
            response = requests.get(url, headers=headers)
            films = response.json()
    text = "Search for ".format(search_term)
    search = "search_movies"
    return render_template("movies.html",films = films,text = text,search_bar_fun =search)

# series pages 
@app.route('/series',methods=["GET", "POST"])
def series():
    insert_data_watchlist('series')
    rawData = requests.get("https://api.themoviedb.org/3/tv/popular?api_key=46eb63b8b7f02741767b041992f640ee")
    series =rawData.json()
    search = 'Search_series'
    text = 'Trending Series'
    placeholder = 'Series'
    return render_template("series.html",series = series ,search_bar_fun =search,placeholder=placeholder ,text= text)

@app.route('/series_page/<id>')
def series_page(id):
    url = "https://api.themoviedb.org/3/tv/{}?language=en-US".format(id)
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_api_key}"
        }
    response = requests.get(url, headers=headers)
    serie = response.json()
    return render_template("serie.html",serie = serie)

@app.route('/series/search',methods=["POST","GET"])
def Search_series():
    series = None
    if request.method == "POST":
        if request.form.get('action') == 'watchlist':
            insert_data_watchlist('movie')
            search_term = session.get('search_result')
            if search_term:
                url = "https://api.themoviedb.org/3/search/movie?query={}&include_adult=false&language=en-US&page=1".format(search_term)
                headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {tmdb_api_key}"
                }
                response = requests.get(url, headers=headers)
                series = response.json()
        else :
            session['search_result'] = request.form.get("main_searchbar")
            search_term = session.get('search_result')
            print(search_term)
            url = "https://api.themoviedb.org/3/search/tv?query={}&include_adult=false&language=en-US&page=1".format(search_term)
            headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {tmdb_api_key}"
            }
            response = requests.get(url, headers=headers)
            series = response.json()
    text = 'Search result for {}'.format(search_term)
    search ="Search_series"
    return render_template("series.html",series = series, text =text,search_bar_fun =search)

# anime pages 
@app.route('/anime',methods=["POST","GET"])
def anime():
    if request.method == 'POST':
        insert_data_watchlist('anime')
    rawData = requests.get("https://api.jikan.moe/v4/top/anime?type=tv&limit=20")
    anime_list = rawData.json()
    text = 'New Animes '
    search = 'anime_search'
    placeholder= 'Anime'
    return render_template("anime.html",anime = anime_list, text =text, search_bar_fun =search,placeholder= placeholder)

@app.route('/singleAnime/<id>')
def anime_data(id):
    rawData = requests.get("https://api.jikan.moe/v4/anime/"+id)
    animedetail = rawData.json()
    return render_template("anime-detail.html", ani = animedetail)

@app.route('/search/anime_search',methods=["POST","GET"])
def anime_search():
    anime_list = None
    if request.method == 'POST':
        if request.form.get("action") == "watchlist":
            insert_data_watchlist('anime')
            search_term = session.get('search_result')
            rawdData = requests.get("https://api.jikan.moe/v4/anime?q="+search_term)
            anime_list = rawdData.json()    
        else :
            session['search_result'] = request.form.get("main_searchbar")
            search_term = session.get('search_result')
            rawdData = requests.get("https://api.jikan.moe/v4/anime?q="+search_term)
            anime_list = rawdData.json()    
    placeholder ='Anime'
    text ='Search Results for '+search_term
    search = 'anime_search'
    return render_template("anime.html",anime =anime_list,text = text,placeholder= placeholder,search_bar_fun =search)

# watchlist page
@app.route('/watchlist', methods=['GET','POST'])
def watchlist():
    user_id = session.get('user_id')
    if request.method == "POST":
        Id = request.form.get("Id")
        click_action = request.form.get('action')
        if click_action == 'watchlist':
            dbconnect.Delete_movie(user_id,Id)
    data = dbconnect.Fetch_all_movies(user_id)
    placeholder = 'Movies'
    search= "search_movies"
    return render_template("watchlist.html",data = data, placeholder=placeholder, search_bar_fun =search)

# completed pages for all movies and animes
@app.route('/completed', methods=['GET','POST'])
def completed():
    user_id = session.get('user_id')
    if request.method == "POST":
        Id = request.form.get("Id")
        click_action = request.form.get('action')
        if click_action == 'watchlist':
            dbconnect.Delete_movie(user_id,Id)
    data = dbconnect.Fetch_all_movies(user_id)
    placeholder = 'Movies'
    search= "search_movies"
    return render_template("watchlist.html",data = data, placeholder=placeholder, search_bar_fun =search)


if __name__ == '__main__':
    app.run(debug=True)