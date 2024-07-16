class Album:
    def __init__(self, name, artist, genre, releaseDate, rank):
        self.name = name
        self.artist = artist
        self.genre = genre
        self.releaseDate = releaseDate
        self.rank = rank
        
    def __str__(self):
        return f"Rank: {self.rank}, Album: {self.name}, Artist: {self.artist}, Genre: {self.genre}, Release Date: {self.releaseDate}"
    