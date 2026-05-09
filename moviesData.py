import mysql.connector as connection 

class moviesdatabase():
    def __init__(self):
        self.connector = connection.connect( host = 'localhost' ,port = 3306, user='root', password='chetan' ,database='watchverse')
        query = 'create table if not exists watchlist(Id interger primary key ,Title varchar(50), Poster varchar(100) , Rating varchar(10) )'
        curser = self.connector.cursor()
        curser.execute(query)
    
    def insert_movies(self,Id,Title, Poster, Rating):
        query = 'insert into watchlist(Title,Poster,Year) values({},"{}","{}","{}" )'.format(Id,Title,Poster,Rating)
        curser = self.connector.cursor()
        curser.execute(query)
        self.connector.commit()

    def Fetch_all_movies(self):
        query = 'select * from watchlist'
        curser = self.connector.cursor()
        curser.execute(query)
        return curser
    
    def Delete_movie(self , Id):
        query = 'delete from watchlist where Title = "{}"'.format(Id)
        curser = self.connector.cursor()
        curser.execute(query)
        self.connector.commit()
