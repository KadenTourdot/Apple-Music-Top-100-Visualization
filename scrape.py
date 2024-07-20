import requests
from album import Album
from spotify import Spotify
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class Scrape:

    def __init__(self, accessCode):
        self.baseUrl = "https://musicbrainz.org/ws/2/"
        self.htmlContent = None
        self.spotify = Spotify(accessCode)

    def scrapeAlbumInfo(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)

        try:

            driver.get(url)
            time.sleep(5)
            button = driver.find_element(
                By.CSS_SELECTOR, 'button[data-testid="subnavicons-index"]'
            )
            button.click()
            time.sleep(15)

            self.htmlContent = driver.page_source

        finally:
            driver.quit()

    def findAlbums(self, htmlContent):
        soup = BeautifulSoup(htmlContent, "html.parser")

        albumElements = soup.find_all("img", alt=True)
        processedAlbums = {}

        rank = 100

        for album in albumElements:
            altText = album["alt"]
            try:
                albumName, artist = altText.split(" - ")
                if albumName not in processedAlbums:
                    processedAlbums[albumName] = {
                        "rank": rank,
                        "albumName": albumName.strip(),
                        "artist": artist.strip(),
                    }
                    rank -= 1
            except ValueError:
                continue

        return processedAlbums

    def enrichAlbums(self, albums):
        enrichedAlbums = []
        for item in albums.values():
            releaseDate, genre = self.spotify.getAlbumInfo(
                item["albumName"], item["artist"]
            )
            enrichedAlbums.append(
                Album(
                    item["albumName"], item["artist"], genre, releaseDate, item["rank"]
                )
            )

        return enrichedAlbums
