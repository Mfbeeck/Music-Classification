# importing the requests library
import requests
import requests.auth
# Import the json library
import json
import sys
import numpy as np
import pandas as pd

def get_playlisted_songs_df(list_of_urls, token):
    token = token
    count=0
    for url in list_of_urls:
        if count == 0:
            df = get_playlist_songs(url, token)
        else:
            df = df.append([get_playlist_songs(url, token)])
        count+=1
    final_data = df.drop_duplicates(subset=['track_id'], keep="first", inplace=False).reset_index(drop=True)
    list_of_data = final_data.values.tolist()
    return list_of_data

# Function to get songs from a playlist
def get_playlist_songs(playlist_url, token):
    # Getting token
    access_token = token

    # splitting given url to grab user id and playlist id
    playlistsplit = playlist_url.split('/playlist/')
    user_id = playlistsplit[0].split('/user/')[1]
    playlist_id = playlistsplit[1].split('?')[0]

    # Getting playlist name to tag onto every track
    # Formatting url into spotify get playlist api call to get playlist name
    play_url = "https://api.spotify.com/v1/users/" + user_id + "/playlists/" + playlist_id
    play_headers={"access_token":access_token}
    play_req=requests.get(play_url, play_headers).text
    playlist_name = json.loads(play_req)['name']

    # Formatting url into spotify playlist tracks api call url
    url = "https://api.spotify.com/v1/users/" + user_id + "/playlists/" + playlist_id +"/tracks"

    offset = 0
    headers={"access_token":access_token, "limit":"100","offset":str(offset)}
    req=requests.get(url, headers).text
    all_json = json.loads(req)
    tracks = all_json['items']
    offset+=100

    # Checking if there are more than 100 songs in playlist, if so, go to next page
    while all_json['next'] != None:
        headers={"access_token":access_token, "limit":"100","offset":str(offset)}
        req=requests.get(url, headers).text
        all_json = json.loads(req)
        tracks = tracks + all_json['items']
        offset+=100

    # Reading and parsing json for to make playlist tracks dataframe
    track_names = []
    track_ids = []
    track_previews = []
    durations = []
    explicits = []
    popularities = []
    artist_names = []
    artist_ids = []
    album_names = []
    album_ids = []
    album_arts = []
    date_addeds = []
    playlist_ids = []
    playlist_names = []

    for song in tracks:
        playlist_names.append(playlist_name)
        playlist_ids.append(playlist_id)
        track_names.append(song['track']['name'])
        track_ids.append(song['track']['id'])
        track_previews.append(song['track']['preview_url'])
        artist_names.append(song['track']['artists'][0]['name'])
        artist_ids.append(song['track']['artists'][0]['id'])
        album_names.append(song['track']['album']['name'])
        album_ids.append(song['track']['album']['id'])
        album_arts.append(song['track']['album']['images'][0]['url'])
        date_addeds.append(song['added_at'])
        durations.append(song['track']['duration_ms'])
        explicits.append(song['track']['explicit'])
        popularities.append(song['track']['popularity'])

    # Chunking Tracks and artists For Several Track/artist Api Call
    track_features_jsons = []
    artist_features_jsons = []
    for i in range(0, len(track_ids), 50):
        # Getting several artists features in one call
        artists_url = "https://api.spotify.com/v1/artists?ids="+(",".join(artist_ids[i:(i+50)]))
        headers={"access_token":access_token}
        req=requests.get(artists_url, headers).text
        all_artists_json = json.loads(req)
        artist_features_jsons.append(all_artists_json)

        # Getting several tracks features in one call
        tracks_url = "https://api.spotify.com/v1/audio-features/?ids="+(",".join(track_ids[i:(i+50)]))
        req=requests.get(tracks_url, headers).text
        all_tracks_json = json.loads(req)
        track_features_jsons.append(all_tracks_json)

    # Iterating in blocks of 20 to get "several album" call urls and hitting api
    album_features_jsons = []
    for i in range(0, len(album_ids), 20):
        # Getting several albumms features in one call
        albums_url = "https://api.spotify.com/v1/albums/?ids="+(",".join(album_ids[i:(i+20)]))
        req=requests.get(albums_url, headers).text
        all_albums_json = json.loads(req)
        album_features_jsons.append(all_albums_json)

    # Getting track features from each track
    acousticness = []
    danceability = []
    energy = []
    instrumentalness = []
    key = []
    liveness = []
    loudness = []
    mode = []
    speechiness = []
    tempo = []
    time_signature = []
    valence = []
    artist_followers = []
    artist_genres = []
    artist_imgs = []
    artist_popularity = []
    release_date_precision = []
    release_date = []
    album_popularity = []

    # Looping over json of tracks features
    for tracks_list in track_features_jsons:
        for track in tracks_list['audio_features']:
            try:
                acousticness.append(track['acousticness'])
                danceability.append(track['danceability'])
                energy.append(track['energy'])
                instrumentalness.append(track['instrumentalness'])
                key.append(track['key'])
                liveness.append(track['liveness'])
                loudness.append(track['loudness'])
                mode.append(track['mode'])
                speechiness.append(track['speechiness'])
                tempo.append(track['tempo'])
                time_signature.append(track['time_signature'])
                valence.append(track['valence'])
            except:
                acousticness.append(None)
                danceability.append(None)
                energy.append(None)
                instrumentalness.append(None)
                key.append(None)
                liveness.append(None)
                loudness.append(None)
                mode.append(None)
                speechiness.append(None)
                tempo.append(None)
                time_signature.append(None)
                valence.append(None)

    # Looping over json of albums
    for albums_list in album_features_jsons:
        for album in albums_list['albums']:
            release_date_precision.append(album['release_date_precision'])
            release_date.append(album['release_date'])
            album_popularity.append(album['popularity'])

    # Looping over json of artists
    for artists_list in artist_features_jsons:
        for artist in artists_list['artists']:
            artist_followers.append(artist['followers']['total'])
            artist_genres.append(artist['genres'])
            try:
                artist_imgs.append(artist['images'][0]['url'])
            except:
                artist_imgs.append(None)
            artist_popularity.append(artist['popularity'])
#         except:
#             artist_followers.append(None)
#             artist_genres.append(None)
#             artist_imgs.append(None)
#             artist_popularity.append(None)

    df_columns = ['playlist_name', 'playlist_id', 'track', 'track_id', 'artist_name',\
                  'duration', 'explicit', 'track_popularity', 'acousticness',\
                  'danceability', 'energy', 'instrumentalness', 'key', 'liveness',\
                  'loudness', 'mode', 'speechiness', 'tempo', 'time_signature',\
                  'valence', 'artist_id', 'artist_followers', 'artist_genre',\
                  'artist_img', 'artist_popularity','album', 'album_popularity', 'album_id', 'album_art',\
                  'album_release_date', 'release_date_precision', 'date_added_to_playlist', 'preview_url']
    playlist_df = pd.DataFrame(list(zip(playlist_names, playlist_ids, track_names,\
                                        track_ids, artist_names, durations,\
                                        explicits, popularities, acousticness, danceability,\
                                        energy, instrumentalness, key, liveness, loudness,\
                                        mode, speechiness, tempo, time_signature, valence,\
                                        artist_ids, artist_followers, artist_genres,\
                                        artist_imgs, artist_popularity, album_names, album_popularity, \
                                        album_ids, album_arts, release_date, release_date_precision, \
                                        date_addeds, track_previews)),\
                               columns=df_columns)

    playlist_df['explicit'] = playlist_df.explicit.astype(int)
    genres=['pop','rap', 'dance pop', 'pop rap', 'post-teen pop', 'hip hop', 'rock', 'trap music', 'modern rock', 'latin', 'edm', 'tropical house', 'southern hip hop', 'r&b', 'classic rock', 'indie r&b', 'album rock', 'reggaeton', 'pop rock', 'post-grunge', 'tropical', 'neo mellow', 'alternative metal', 'latin pop', 'mellow gold', 'urban contemporary', 'singer-songwriter', 'soft rock', 'permanent wave', 'nu metal']
    for x in genres:
        genre_rows = []
        for index, row in playlist_df.iterrows():
            try:
                if x in row['artist_genre']:
                    genre_rows.append(1)
                else:
                    genre_rows.append(0)
            except:
                genre_rows.append(0)
        playlist_df[x] = genre_rows

    return playlist_df

json.dump(get_playlisted_songs_df(sys.argv[1].split(","), sys.argv[2]), sys.stdout)
