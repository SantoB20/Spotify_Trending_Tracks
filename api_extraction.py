from dotenv import load_dotenv
import os
import base64
import requests
import json
import pandas as pd

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

playlists = {
    'Top-50-Colombia': '37i9dQZEVXbOa2lmxNORXQ',
    'Top-50-Mexico': '37i9dQZEVXbO3qyFxbkOE1',
    'Top-50-Spain': '37i9dQZEVXbNFJfN1Vw8d9',
    'Top-50-Argentina': '37i9dQZEVXbMMy2roB9myp',
    'Top-50-Venezuela': '37i9dQZEVXbNLrliB10ZnX',
    'Top-50-Chile': '37i9dQZEVXbL0GavIqMTeb',
    'Top-50-Ecuador': '37i9dQZEVXbJlM6nvL1nD1',
    'Top-50-Dominican-Republic': '37i9dQZEVXbKAbrMR8uuf7',
    'Top-50-Peru': '37i9dQZEVXbJfdy5b0KP7W',
    'Top-50-Panama': '37i9dQZEVXbKypXHVwk1f0',
    'Top-50-Uruguay': '37i9dQZEVXbMJJi3wgRbAy',
    'Top-50-Paraguay': '37i9dQZEVXbNOUPGj7tW6T',
    'Top-50-Bolivia': '37i9dQZEVXbJqfMFK4d691',
    'Top-50-Costa-Rica': '37i9dQZEVXbMZAjGMynsQX',
    'Top-50-Guatemala': '37i9dQZEVXbLy5tBFyQvd4',
    'Top-50-Honduras': '37i9dQZEVXbJp9wcIM9Eo5',
    'Top-50-El-Salvador': '37i9dQZEVXbLxoIml4MYkT',  
}

def get_token():
    auth = client_id + ':' + client_secret
    auth_bytes = auth.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes),'utf-8')
    
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    
    response = requests.post(url, headers=headers, data=data)
    return json.loads(response.content)['access_token']
    
def auth_headers(token):
    return {'Authorization': 'Bearer ' + token}

def get_playlist_tracks(token, playlist_id, playlist_name):
    url = 'https://api.spotify.com/v1/playlists/' + playlist_id
    headers = auth_headers(token)
    
    response = requests.get(url, headers=headers)
    
    return [{'id': track['track']['id'],
             'name': track['track']['name'],
             'explicit': track['track']['explicit'],
             'release_date': track['track']['album']['release_date'],
             'artist': track['track']['artists'][0]['name'],
             'popularity': track['track']['popularity'],
             'playlist': playlist_name
             } for track in json.loads(response.content)['tracks']['items']]

def get_track_audio_features(token, track_id):
    url = 'https://api.spotify.com/v1/audio-features/' + track_id
    headers = auth_headers(token)
    
    response = requests.get(url, headers=headers)
    
    response_json = json.loads(response.content)
    for key in ['analysis_url','id','track_href','type','uri']:
        response_json.pop(key)
    
    return response_json

token = get_token()
tracks = []
for key, value in playlists.items():
    tracks.extend(get_playlist_tracks(token,value,key))
    
for track in tracks:
    track.update(get_track_audio_features(token, track['id']))

tracks_df = pd.DataFrame.from_dict(tracks)
tracks_df.to_excel('top_tracks_latin_playlists.xlsx', sheet_name='tracks', index= False)