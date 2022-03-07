import string
import pandas as pd
import os
import re
import requests
import csv
from tqdm import tqdm
import sys
sys.path.append("..")
import preprocessing

!pip install git+git://github.com/dbeley/rymscraper.git@master
!pip install git+https://github.com/johnwmillr/LyricsGenius.git
import lyricsgenius
from bs4 import BeautifulSoup
from pathlib import Path

import pandas as pd
from rymscraper import rymscraper, RymUrl

network = rymscraper.RymNetwork()

client_access_token = "Ob87cTycMnGhXLCozaho1Ow0IWJZGT5iy_Xk7_3TTXz5tstLYjFeVXemNQkKEHQkX82uJotzT_sgjWSfhWtMgw"

def get_album_info(album_name, artist_name):
    LyricsGenius = lyricsgenius.Genius(client_access_token, timeout=10, retries = 3)
    LyricsGenius.remove_section_headers = True

    info = [album_name]

    try:
        album_object = LyricsGenius.search_album(album_name, artist_name)
        date_object = album_object.release_date_components
        date = f"{date_object.year}-{date_object.month}-{date_object.day}"
        info.append(date)
    except:
        info.append("")

    try:
        info.append(album_object.cover_art_thumbnail_url)
    except:
        info.append("")

    return info


def get_genres(artist, album):
    try:
        album_infos = network.get_album_infos(name=f"{artist} - {album}")
        return album_infos['Genres'].split('\n')[0]
    except:
        pass

    try:
        artist = artist.lower().replace(' ', '-')
        album = album.lower().replace(' ', '-')
        album_infos = network.get_album_infos(url=f"https://rateyourmusic.com/release/album/{artist}/{album}/")
        return album_infos['Genres'].split('\n')[0]
    except:
        return ""


with open('./data/songs_info.csv','w',encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["song_id", "song_name", "artist_name", "album_name", "release_date", "album_cover_url", "genres"])

album_list = []
with open('./data/songs_list.csv','r',encoding='utf-8') as csvreader:
    reader = csv.reader(csvreader)
    next(reader)
    for row in reader:
        song_id = row[0]
        song_name = row[1]
        artist_name = row[2]
        album_name = row[3]
        print(song_id)
        song_info = [song_id, song_name, artist_name]
        if album_name not in album_list:
            album_list.append(album_name)
            album_info = get_album_info(album_name, artist_name)
            album_info.append(get_genres(artist_name,album_name))

        song_info.extend(album_info)
        with open('./data/songs_info.csv','a',encoding='utf-8', newline='') as csvwriter:
            writer = csv.writer(csvwriter)
            writer.writerow(song_info)


alllyrics=pd.read_csv("./data/sentences.csv")
df=alllyrics.dropna(subset=['Sentence'])
df=df.reset_index(drop=True)
df.to_csv('./data/sentences.csv',index=False)


data = pd.read_csv("./data/songs_info.csv")
alllyrics=pd.read_csv('./data/sentences.csv')
alllyrics
lyrics_dict={}

for songid in tqdm(data['song_id']):
    lyrics_dict[songid]=list(alllyrics[alllyrics['Song_id']==songid]['Sentence'])

df=data
df['lyrics'] = df['song_id'].map(lyrics_dict)
df['album_cover_url'] = df['album_cover_url'].fillna("https://p.turbosquid.com/ts-thumb/jO/8hrD0I/WY/247vinyl_phonograph_record0001/jpg/1640965984/300x300/sharp_fit_q85/386c57a9f06bac781219d6b6e3a7b72a785bbebe/247vinyl_phonograph_record0001.jpg")
df['release_date'] = df['release_date'].fillna("UNKNOWN")
df['genres'] = df['genres'].fillna("UNKNOWN")
df.to_json ('./data/songs_info.json',orient='records')

data = pd.read_json("./data/songs_info.json")
data["song_name_preprocess"] = data.song_name.map(preprocessing.preprocess)
data["artist_name_preprocess"] = data.artist_name.map(preprocessing.preprocess)
data["album_name_preprocess"] = data.album_name.map(preprocessing.preprocess)
df = data
df.to_json ('./data/songs_info.json',orient='records')
