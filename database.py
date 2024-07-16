import mysql.connector

class Database:

    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS albums (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            artist VARCHAR(255),
            genre VARCHAR(255),
            releaseDate DATE,
            top100Rank INT
        )''')

    def insert_album(self, album):
        try:
            sql = "INSERT INTO albums (name, artist, genre, releaseDate, top100Rank) VALUES (%s, %s, %s, %s, %s)"
            val = (album.name, album.artist, album.genre, album.releaseDate, album.rank)
            self.cursor.execute(sql, val)
            self.conn.commit()
            print("Album inserted successfully")
        except Error as e:
            print(f"The error '{e}' occurred")