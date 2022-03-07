import csv
import os
import re

def get_filelist(dir):
    Filelist = []
    for home, dirs, files in os.walk(dir):
        for filename in files:
            Filelist.append(os.path.join(home, filename))

    return Filelist


path ='./data/all_songs_lyrics'
Filelist = get_filelist(path)

whole_lyrics = []
song_num = 0
with open('songs_list.csv','w',encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["song_id", "song_name", "artist_name", "album_name"])

for file in Filelist[1:]:
    song_num += 1
    song_id = f"s{song_num}"
    file_str = file.split('/')
    song_name = file_str[-1][:-4]
    artist_and_album = file_str[-2].split('_')
    artist_name = artist_and_album[0]
    album_name = artist_and_album[1]
    with open('songs_list.csv','a',encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([song_id, song_name, artist_name, album_name])
