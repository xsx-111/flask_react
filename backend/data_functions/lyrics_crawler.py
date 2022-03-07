!pip install git+https://github.com/johnwmillr/LyricsGenius.git
import string
import pandas as pd
import os
import re
import requests
import lyricsgenius
from bs4 import BeautifulSoup
from pathlib import Path

def download_album_lyrics(artist, album_name):

    LyricsGenius = lyricsgenius.Genius(client_access_token, timeout=10, retries = 3)
    LyricsGenius.remove_section_headers = True

    album_object = LyricsGenius.search_album(album_name, artist)

    #artist_title = artist.replace(" ", "-")
    #album_title = album_name.replace(" ", "-")
    old_directory = os.getcwd()

    if album_object == None:
        with open('NO_RESULTS_LIST', 'a') as f:
            f.write(f"{album_name} by {artist}\n")

    else:
        artist = artist.replace("/", "-")
        album_name = album_name.replace("/", "-")
        new_directory = f"{artist}_{album_name}"
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)
        os.chdir(new_directory)
        for song_object in album_object.tracks:
            if song_object._body['number'] == None:
                continue

            if song_object.song.title.isascii() == False:
                continue

            song = song_object.song.title.replace("/", "-")

            if os.path.exists(f"{song}.txt"):
                continue

            song_object.song.save_lyrics(filename=song, extension='txt', sanitize=False)

    os.chdir(old_directory)

client_access_token = "dvKDeEZA-0K5s8AyTYK0V6FhKjQ47OAbx-GSbPFmTZhoXTVnyrKq2GDN8mcM_i8A"
old_directory = os.getcwd()
new_directory = 'data/all_songs_lyrics'

albums = pd.read_csv("10000albums.csv")
#chars_to_remove = re.compile(f'[{string.punctuation}]')
titles_and_artists = []

i=2
while True:
    try:
        title = albums.iloc[i]['Title']
        artist = albums.iloc[i]['Band']
        if title.isascii() and artist.isascii():
            titles_and_artists.append((artist, title))
        i += 1
    except:
        break

if not os.path.exists(new_directory):
    os.makedirs(new_directory)
os.chdir(new_directory)

for j in range(len(titles_and_artists)):
    download_album_lyrics(titles_and_artists[j][0], titles_and_artists[j][1])
os.chdir(old_directory)
