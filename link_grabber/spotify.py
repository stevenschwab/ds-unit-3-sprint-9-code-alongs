'''Module for Spotify API authentication'''

import requests
from os import getenv

def authenticate():
    """
    Authenticate with Spotify API using client credentials flow.
    Returns the access token if successful, raises an exception otherwise.
    """
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
            'client_secret': getenv('CLIENT_SECRET'),
        }
    )

    # Check response status
    if auth_response.status_code != 200:
        raise Exception(f"Authentication failed: {auth_response.json()}")

    # convert the response to JSON and extract access token
    auth_response_data = auth_response.json()
    # save the access token
    access_token = auth_response_data['access_token']
    return access_token
