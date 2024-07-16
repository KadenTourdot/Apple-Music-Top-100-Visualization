import album
import requests
import json 
from dateutil import parser

class Spotify:

    def __init__(self, accessCode):
        self.accessCode = accessCode

    def getAlbumInfo(self, albumName, artist):
        search_url = "https://api.spotify.com/v1/search"
        headers = {
            "Authorization": f"Bearer {self.accessCode}"
        }
        params = {
            "q": f'album:"{albumName}" artist:"{artist}"',
            "type": "album",
            "limit": 1
        }
        response = requests.get(search_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'albums' in data and data['albums']['items']:
                albumData = data['albums']['items'][0]
                albumId = albumData.get('id', None)
                if albumId:
                    albumUrl = f"https://api.spotify.com/v1/albums/{albumId}"
                    albumResponse = requests.get(albumUrl, headers=headers)
                    if albumResponse.status_code == 200:
                        albumDetails = albumResponse.json()
                        releaseDate = albumDetails.get('release_date', None)
                        genre = self.getArtistGenre(artist)
                        normalDate = self.normalizeDate(releaseDate)
                        return normalDate, genre
                    
        return None, None
    
    def normalizeDate(self, date):
        try:
            normalDate = parser.parse(date)
            return normalDate.strftime('%Y-%M-%D')
        except parser.ParserError:
            return None

    def getArtistGenre(self, artistName):
        searchUrl = "https://api.spotify.com/v1/search"
        headers = {
            "Authorization": f"Bearer {self.accessCode}"
        }
        params = {
            "q": f'artist:"{artistName}"',
            "type": "artist",
            "limit": 1
        }
        response = requests.get(searchUrl, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'artists' in data and data['artists']['items']:
                artistData = data['artists']['items'][0]
                genres = artistData.get('genres', [])
                genre = genres[0] if genres else 'Could not be found'
                return genre
            
        return "Could not be found"




