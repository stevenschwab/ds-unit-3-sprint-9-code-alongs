'''
Module for Spotify API authentication
and get album/track functions
'''
import requests
from os import getenv


def authenticate():
    '''
    Authenticate with Spotify API using client credentials flow.
    Returns the access token if successful; raises an exception  otherwise.
    '''
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST request with form-urlencoded data
    auth_response = requests.post(
        AUTH_URL,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'grant_type': 'client_credentials',
            'client_id': getenv('CLIENT_ID'),
            'client_secret': getenv('CLIENT_SECRET')
        }
    )

    # Check response status
    if auth_response.status_code != 200:
        raise Exception(f'Authentication failed: {auth_response.json()}')

    # convert the response to JSON and extract access token
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    return access_token


BASE_URL = 'https://api.spotify.com/v1/'


def get_album(album_id):
    '''
    Get an album from the Spotify API using the authentication flow.
    Returns the album response if successful; raises an exception otherwise.
    '''
    # get an authentication token
    token = authenticate()

    # add authentication token to the request headers
    headers = {
        'Authorization': 'Bearer {token}'.format(token=token)
    }
    query_url = BASE_URL + f'albums/{album_id}'
    response = requests.get(
        query_url,
        headers=headers
    )

    # check response status
    if response.status_code != 200:
        raise Exception(f'Get album failed: {response.json()}')

    # convert the response to JSON
    response_data = response.json()
    return response_data


def get_track(track_id):
    '''
    Get a track from the Spotify API using the authentication flow.
    Returns the track response if successful; raises an exception otherwise.
    '''
    # get an authentication token
    token = authenticate()

    # add authentication token to the request headers
    headers = {
        'Authorization': 'Bearer {token}'.format(token=token)
    }
    query_url = BASE_URL + f'tracks/{track_id}'
    response = requests.get(
        query_url,
        headers=headers
    )

    # check response status
    if response.status_code != 200:
        raise Exception(f'Get track failed: {response.json()}')

    # convert the response to JSON
    response_data = response.json()
    return response_data


if __name__ == '__main__':
    pass
    # print(get_album('5BWl0bB1q0TqyFmkBEupZy'))
    # print(get_track('75FEaRjZTKLhTrFGsfMUXR'))
