import mysql.connector as connector

class DatabaseConnect():
    def __init__(self):
        self.database_connect = connector.connect(host = "localhost", user="root", password="chetan", port=3306, database="WatchVerse")
        query = 'create table if not exists User(UserId varchar(50) primary key, name varchar(50),email varchar(50),password varchar(100) ) '
        cursor = self.database_connect.cursor()
        cursor.execute(query)

    def Insert_user(self, userid, name, email, password):
        query='insert into User(UserId , name, email,password ) value( "{}", "{}", "{}" , "{}" )'.format(userid,name,email,password)
        cursor = self.database_connect.cursor()
        cursor.execute(query)
        self.database_connect.commit()
    
    def Fetch_Password(self, email):
        query = 'select name,password from user where email = "{}"'.format(email)
        cursor = self.database_connect.cursor()
        cursor.execute(query)
        return cursor