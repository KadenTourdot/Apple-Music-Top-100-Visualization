from scrape import Scrape
import requests
from database import Database



def main():
    webScraper = Scrape('BQAy3e9u1GnEjdjbOqANZvs4gGjL14nUL76fr7rGvQqnn5nGE8xY8hQq4AL8S6isHINBZ70cMT4MzOd4z4OhaOcvh7Fd77LNP3peDDYmT55aSqwIBhQ')
    webpageUrl = 'https://100best.music.apple.com/us'
    webScraper.scrapeAlbumInfo(webpageUrl)
    albums = webScraper.findAlbums(webScraper.htmlContent)
    enrichedAlbums = webScraper.enrichAlbums(albums)

    db = Database(host = 'localhost', user = "root", password = "password", database = 'top100')
    db.create_table()
    
    for album in enrichedAlbums:
          db.insert_album(album)



def get_spotify_token():
        client_id = ''
        client_secret = ''
        auth_url = 'https://accounts.spotify.com/api/token'
        auth_response = requests.post(auth_url, {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        })
        auth_response_data = auth_response.json()
        return auth_response_data['access_token']
main()




