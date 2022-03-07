import csv
import os
import re

def get_filelist(dir):
    Filelist = []
    for home, dirs, files in os.walk(dir):
        for filename in files:
            Filelist.append(os.path.join(home, filename))

    return Filelist


path='./data/all_songs_lyrics'
Filelist = get_filelist(path)

whole_lyrics = []
song_num = 0

with open('data/sentences.csv','w',encoding='utf-8', newline='') as f2:
    writer = csv.writer(f2)
    writer.writerow(['Sentence','Song_id','Song_name'])

for file in Filelist[1:]:
    song_num += 1
    song_id = f"s{song_num}"
    with open(file,'r',encoding='utf-8') as f1:
        content = f1.readlines()
        if len(content) == 0:
            continue

        song_name=file.split('/')[-1][:-4]

        if " Lyrics" in content[0]:
            content[0] = content[0].split(" Lyrics")[1]

        for i,line in enumerate(content):
            if line == "\n" or len(line) == 0 or line == '\t':
                continue

            if i == len(content)-1:
                line = re.split('[0-9]*Embed', line)[0]

            with open('data/sentences.csv','a',encoding='utf-8', newline='') as f2:
                writer = csv.writer(f2)
                writer.writerow([line.strip('\n'), song_id, song_name])
