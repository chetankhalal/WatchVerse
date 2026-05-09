import mysql.connector as connector

class DatabaseConnect():
    def __init__(self):
        self.database_connect = connector.connect(host = "localhost", user="root", password="chetan", port=3306, database="WatchVerse")
        query = 'create table if not exists users(user_id INT PRIMARY KEY AUTO_INCREMENT, username varchar(50),email varchar(50) unique ,password varchar(100) ) '
        cursor = self.database_connect.cursor()
        cursor.execute(query)
        query = 'create table if not exists movies(movie_id INT PRIMARY KEY ,title VARCHAR(255) NOT NULL,type ENUM("movie", "anime", "series") NOT NULL, Poster varchar(255) , Rating varchar(10))'
        cursor.execute(query)
        query = 'create table if not exists watchlist(user_id INT NOT NULL,movie_id INT NOT NULL,added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (user_id, movie_id),FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE)'
        cursor.execute(query)

    def Insert_user(self, name, email, password):
        query='insert into users(username, email,password ) value( "{}", "{}" , "{}" )'.format(name,email,password)
        cursor = self.database_connect.cursor()
        cursor.execute(query)
        self.database_connect.commit()
    
    def Fetch_Password(self, email):
        query = 'select user_id, username, password from users where email = "{}"'.format(email)
        cursor = self.database_connect.cursor()
        cursor.execute(query)
        return cursor
    
    def insert_movies(self,Id,Title,Type, Poster, Rating ):
        query = 'insert IGNORE into movies(movie_id,Title,type,Poster,Rating) values({},"{}","{}","{}" ,{})'.format(Id,Title,Type,Poster,Rating)
        curser = self.database_connect.cursor()
        curser.execute(query)
        self.database_connect.commit()

    def get_movie_by_id(self,movie_id):
        query = "select title from movies where movie_id = {}".format(movie_id)
        curser = self.database_connect.cursor()
        curser.execute(query)
        return curser

    def insert_watchlist(self,user_id, movie_id):
        query = 'INSERT IGNORE INTO watchlist (user_id, movie_id) VALUES ({},{})'.format(user_id,movie_id)
        cursor = self.database_connect.cursor()
        cursor.execute(query)
        self.database_connect.commit()

    def Fetch_all_movies(self,user_id):
        query = 'SELECT m.movie_id, m.title,m.type, m.poster, m.rating FROM watchlist w JOIN movies m ON w.movie_id = m.movie_id WHERE w.user_id = {}'.format(user_id)
        curser = self.database_connect.cursor()
        curser.execute(query)
        return curser
    
    def Delete_movie(self , user_id, movie_id ):
        query = 'DELETE FROM watchlist WHERE user_id = {} AND movie_id = {}'.format(user_id,movie_id)
        curser = self.database_connect.cursor()
        curser.execute(query)
        self.database_connect.commit()