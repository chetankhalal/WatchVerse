from flask import Flask, render_template, request,redirect, session, url_for
from database import DatabaseConnect
from uuid import uuid4
from flask_bcrypt import Bcrypt
import requests

dbconnect = DatabaseConnect()
userid = uuid4()

app = Flask("__name__")
app.secret_key="login"
bcrypt = Bcrypt(app)

@app.route('/')
def temp():
    return render_template("index.html")

@app.route('/signin', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        userid = str(uuid4())
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
        dbconnect.Insert_user(userid,name,email,hashed_password)
        session['name'] = first_name
        return redirect(url_for('dash'))
    return render_template("signin.html")

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

            name = cursor_list[0][0]
            hash_password = cursor_list[0][1]
            first_name = name.split()[0] if name else 'Guest'
            # check password
            is_valid = bcrypt.check_password_hash(hash_password, password)

            if is_valid:
                session['email'] = email
                session['name'] = first_name       # store name in session too
                return redirect(url_for('dash'))  # redirect instead of render

            else:
                msg = "Invalid password"
                return render_template('login.html', msg=msg)

        except Exception as e:
            print("Error occurred: ", e)
            msg = "Something went wrong. Please try again."
            return render_template('login.html', msg=msg)

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/')

@app.route('/dashboard')
def dash():
    session.get('First_name')
    return render_template("base.html")

@app.route('/series')
def series():
    return render_template("series.html")

@app.route('/movies')
def movies():
    rawData = requests.get('http://www.omdbapi.com/?i=tt3896198&apikey=8f4be22e&s=batman')
    films = rawData.json()
    return render_template("movies.html", films = films)

@app.route('/copy')
def copy():
    return render_template("copy.html")

if __name__ == '__main__':
    app.run(debug=True)