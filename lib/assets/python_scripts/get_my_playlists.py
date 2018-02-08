# importing the requests library
import requests
import requests.auth
# Import the json library
import json
import sys
import numpy as np
import pandas as pd

def get_my_playlists(token):
    url = "https://api.spotify.com/v1/me/playlists"
    private_token = token

    offset = 0
    headers={"access_token":private_token, "limit":"50", "offset":str(offset)}
    req=requests.get(url, headers).text
    all_json = json.loads(req)
    playlists = all_json['items']

    # Only get 50 at a time so iterate over next 50 until finished
    offset+=50

    # Checking if there are more than 50 public playlists
    while all_json['next'] != None:
        headers={"access_token":private_token, "limit":"50","offset":str(offset)}
        req=requests.get(url, headers).text
        all_json = json.loads(req)
        playlists = playlists + all_json['items']
        offset+=50

    # Reading and parsing json for to make list of user's playlists
    playlist_names = []
    owner_names = []
    owner_ids = []
    playlist_arts = []
    playlist_urls = []
    playlist_ids = []
    trackcounts = []
    collaborative_bool = []
    public_bool = []
    # The following are collected from individual playlist calls
    # if profile has many playlists, this might not be worth doing
    # (i.e. spotify has 1600 playlists which yields 1600 more calls to api)
#     descriptions = []
#     followers = []

    for playlist in playlists:
        playlist_names.append(playlist['name'])
        owner_names.append(playlist['owner']['display_name'])
        owner_ids.append(playlist['owner']['id'])
        try:
            try:
                playlist_arts.append(playlist['images'][0]['url'])
            except:
                playlist_arts.append(None)
        except:
            playlist_arts.append(null)
        playlist_urls.append(playlist['external_urls']['spotify'])
        playlist_ids.append(playlist['id'])
        trackcounts.append(playlist['tracks']['total'])
        collaborative_bool.append(playlist['collaborative'])
        public_bool.append(playlist['public'])

#         # Making new request for each playlist to get further details (follower count)
#         playlist_url = "https://api.spotify.com/v1/users/" + playlist['owner']['id'] + "/playlists/" + playlist['id']
#         playlist_req_headers={"access_token":access_token}
#         playlist_req=requests.get(playlist_url, playlist_req_headers).text
#         individ_playlist_json = json.loads(playlist_req)
#         try:
#             descriptions.append(individ_playlist_json['description'])
#         except:
#             descriptions.append(null)
#         try:
#             followers.append(individ_playlist_json['followers']['total'])
#         except:
#             followers.append(null)

    playlist_df = pd.DataFrame(list(zip(playlist_names, trackcounts, owner_names, owner_ids, playlist_urls, playlist_ids, playlist_arts, collaborative_bool, public_bool)),
                  columns=['playlist_name','track_count', 'owner', 'owner_id', 'playlist_url', 'playlist_id', 'playlist_artwork', 'collaborative', 'public'])
    list_of_playlists = playlist_df.values.tolist()
    # print(list(list_of_playlists))
    return(list_of_playlists)

json.dump(get_my_playlists(sys.argv[1]), sys.stdout)
