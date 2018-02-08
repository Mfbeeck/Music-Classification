# importing the requests library
import requests
import requests.auth
# Import the json library
import json
import sys
import spotipy
import spotipy.util as util

def get_token(client_id,client_secret):
    client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    post_data = {"grant_type": "client_credentials"}
    response = requests.post("https://accounts.spotify.com/api/token",
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()
    print(token_json['access_token'])
    return token_json['access_token']

def get_all_tokens(client_id1, client_secret1):
    private_token = spotipy.util.prompt_for_user_token("mfbeeck@gmail.com", scope='user-library-read', client_id=client_id1, client_secret=client_secret1, redirect_uri="http://localhost/")
    access_token = get_token(client_id1, client_secret1)
    tokens = []
    tokens.append(access_token)
    tokens.append(private_token)
    print(tokens)
    return tokens

get_token(sys.argv[1], sys.argv[2])
