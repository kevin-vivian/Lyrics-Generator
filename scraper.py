#!/usr/bin/python
# encoding: utf-8

# https://towardsdatascience.com/using-data-to-find-the-most-brutal-cannibal-corpse-song-bf318d0b3ef4
# https://github.com/rbuerki/most-brutal-cannibal-corpse/blob/master/1-Audio-Analysis.ipynb
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
import credentials
import sys
import requests

''' shows the albums and tracks for a given artist.
'''

# Get Artist URI
def get_artist_uri(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    artist_uri = items[0]['uri']
    return artist_uri

# Get Artist albums (dict)
# Note: setting title as key catches some duplicates
def get_artist_albums(artist_uri):
    albums = {}
    results = sp.artist_albums(artist_uri, album_type='album', limit=25)
    for i, item in enumerate(results['items']):
        albums[item['name'].title()] = item['uri']
    return albums

def get_clean_album_uri_list(artist_albums, albums_to_delete):
    if albums_to_delete is not None:
        for key in albums_to_delete:
            artist_albums.pop(key)
    artist_albums_uri = [uri for uri in artist_albums.values()]
    return artist_albums_uri

# Get the full tracklist
def get_full_tracklist_dict(artist_albums_uri):
    tracklist = {}
    for album_uri in artist_albums_uri:
        album = sp.album(album_uri)
        for track in album['tracks']['items']:
            tracklist[track['name'].title()] = track['uri']
    return tracklist

if __name__ == '__main__':
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    name = "Megadeth"
    artist_uri = get_artist_uri(name)
    pprint(artist_uri)

    artist_albums = get_artist_albums(artist_uri)
    # pprint(artist_albums)

    albums_to_delete = ['Countdown To Extinction: Live',
                        'Dystopia (Deluxe Edition)',
                        'Endgame (2019 - Remaster)',
                        'Endgame (2019 Remaster)',
                        'Rust In Peace Live',
                        'Rust In Peace Live (Ealbum)',
                        'Super Collider (Commentary)',
                        'United Abominations (2019 - Remaster)',
                        'United Abominations (2019 Remaster)',
                        'Warchest',
                        'Warheads On Foreheads',
                        'ライヴ・イン・ニューヨーク1994 (Live At ウェブスター・ホール、ニューヨーク、1994)']
    artist_albums_uri = get_clean_album_uri_list(artist_albums, albums_to_delete)
    pprint(artist_albums_uri)

    full_tracklist = get_full_tracklist_dict(artist_albums_uri)
    pprint(list(full_tracklist.items()))
    print("Total tracks:", len(full_tracklist))

    base = "https://api.genius.com"
    genius_token = credentials.genius_token
    # soup = BeautifulSoup(file, 'html.parser')
