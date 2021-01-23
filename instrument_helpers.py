import sqlite3, requests, json, random
import xml.etree.ElementTree as ET



def getsongsterr():

    artists = ['BTS','Michael Jackson', 'Lady Gaga','ABBA','Aerosmith']
#     songURL = 'https://www.songsterr.com/a/ra/songs/byartists.json'

    songster = requests.get(f'http://www.songsterr.com/a/ra/songs.xml?pattern={random.choice(artists)}')
    root = ET.fromstring(songster.content)
    songs = []
    for child in root:
        songs.append(child.attrib['id'])

    return 'http://www.songsterr.com/a/wa/song?id=' + random.choice(songs)
    

