'''Module for retrieving Spotify Global Top 50 playlist links'''

import requests
from spotify import authenticate

# Spotify global top 50 playlist: https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF


def get_top_50_links():
    """
    Retrieve track URLs from Spotify Global Top 50 playlist.
    Returns a list of track URLs or raises an exception on failure.
    """

    # get an authentication token
    try:
        token = authenticate()
        if not token:
            raise ValueError("No access token received")
    except Exception as e:
        raise Exception(f"Authentication error: {str(e)}")

    # add authentication token to the request headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Spotify Global Top 50 playlist ID
    playlist_id = '3cEYpjA9oz9GiPac4AsH4n'
    query_url = f'https://api.spotify.com/v1/playlists/{playlist_id}'

    # query the spotify api
    response = requests.get(query_url, headers=headers)

    # check response status
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.json()}")

    # parse the response into a dictionary (JSON)
    response_data = response.json()

    # exploring the response object's structure
    # print(response_data)
    # print(len(response))
    # print(response.keys())
    # print(response['tracks'])
    # print(len(response['tracks']))
    # print(response['tracks'].keys())
    # print(response['tracks']['items'])
    # print(len(response['tracks']['items']))
    # print(len(response['tracks']['items'][0].keys()))
    # print(response['tracks']['items'][0]['track']['external_urls']['spotify'])

    # get links to all of the songs in this playlist
    song_links = [song['track']['external_urls']['spotify']
                  for song in response_data['tracks']['items']]

    return song_links


if __name__ == '__main__':
    print(get_top_50_links())
