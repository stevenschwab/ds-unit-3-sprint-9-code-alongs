'''Tests for Media and Song classes'''


import pytest
from unittest.mock import patch
from media_grabber.media import Media, Song


# Mock Spotify API responses
MOCK_ALBUM = {
    'id': '5BWl0bB1q0TqyFmkBEupZy',
    'name': 'Test Album',
    'release_date': '2020-01-01',
    'external_urls': {'spotify': 'https://open.spotify.com/album/5BWl0bB1q0TqyFmkBEupZy'}
}

MOCK_SONG = {
    'id': '75FEaRjZTKLhTrFGsfMUXR',
    'name': 'Test Song',
    'album': {'release_date': '2020-01-01'},
    'external_urls': {'spotify': 'https://open.spotify.com/track/75FEaRjZTKLhTrFGsfMUXR'},
    'explicit': True,
    'duration_ms': 180000,  # 3 minutes
    'disc_number': 1,
    'popularity': 85
}


def test_media_init():
    '''Test Media class initialization'''
    media = Media(
        id=MOCK_ALBUM['id'],
        title=MOCK_ALBUM['name'],
        release_year=MOCK_ALBUM['release_date'],
        href=MOCK_ALBUM['external_urls']['spotify']
    )
    assert media.id == '5BWl0bB1q0TqyFmkBEupZy'
    assert media.title == 'Test Album'
    assert media.release_year == '2020-01-01'
    assert media.href == 'https://open.spotify.com/album/5BWl0bB1q0TqyFmkBEupZy'


def test_media_summary():
    '''Test Media.summary method'''
    media = Media(
        id=MOCK_ALBUM['id'],
        title=MOCK_ALBUM['name'],
        release_year=MOCK_ALBUM['release_date'],
        href=MOCK_ALBUM['external_urls']['spotify']
    )
    expected = '"Test Album" was released in 2020-01-01.\nView ' \
        'this media at https://open.spotify.com/album/5BWl0bB1q0TqyFmkBEupZy'
    assert media.summary() == expected


def test_media_repr():
    """Test Media.__repr__ method"""
    media = Media(
        id=MOCK_ALBUM['id'],
        title=MOCK_ALBUM['name'],
        release_year=MOCK_ALBUM['release_date'],
        href=MOCK_ALBUM['external_urls']['spotify']
    )
    assert str(media) == 'Media: Test Album - 2020-01-01'


def test_song_init():
    """Test Song class initialization"""
    song = Song(
        id=MOCK_SONG['id'],
        title=MOCK_SONG['name'],
        release_year=MOCK_SONG['album']['release_date'],
        href=MOCK_SONG['external_urls']['spotify'],
        explicit=MOCK_SONG['explicit'],
        duration_ms=MOCK_SONG['duration_ms'],
        disc_number=MOCK_SONG['disc_number'],
        popularity=MOCK_SONG['popularity']
    )
    assert song.id == '75FEaRjZTKLhTrFGsfMUXR'
    assert song.title == 'Test Song'
    assert song.release_year == '2020-01-01'
    assert song.href == 'https://open.spotify.com/track/75FEaRjZTKLhTrFGsfMUXR'
    assert song.explicit is True
    assert song.duration_ms == 180000
    assert round(song.duration_mins, 2) == 3.0
    assert song.disc_number == 1
    assert song.popularity == 85


def test_song_summary_explicit():
    """Test Song.summary method for explicit song"""
    song = Song(
        id=MOCK_SONG['id'],
        title=MOCK_SONG['name'],
        release_year=MOCK_SONG['album']['release_date'],
        href=MOCK_SONG['external_urls']['spotify'],
        explicit=True,
        duration_ms=MOCK_SONG['duration_ms'],
        disc_number=MOCK_SONG['disc_number'],
        popularity=MOCK_SONG['popularity']
    )
    expected = 'The song "Test Song" was released in 2020-01-01.\nListen on ' \
        'Spotify: https://open.spotify.com/track/75FEaRjZTKLhTrFGsfMUXR. Be ' \
        'careful, it\'s explicit.'
    assert song.summary() == expected


def test_song_summary_non_explicit():
    """Test Song.summary method for non-explicit song"""
    song = Song(
        id=MOCK_SONG['id'],
        title=MOCK_SONG['name'],
        release_year=MOCK_SONG['album']['release_date'],
        href=MOCK_SONG['external_urls']['spotify'],
        explicit=False,
        duration_ms=MOCK_SONG['duration_ms'],
        disc_number=MOCK_SONG['disc_number'],
        popularity=MOCK_SONG['popularity']
    )
    expected = 'The song "Test Song" was released in 2020-01-01.\nListen on ' \
        'Spotify: https://open.spotify.com/track/75FEaRjZTKLhTrFGsfMUXR'
    assert song.summary() == expected


@pytest.mark.parametrize("duration_ms, expected", [
    (660000, "That song is way too long!"),  # 11 minutes
    (360000, "That is a long son."),         # 6 minutes
    (180000, "That song is medium length"),  # 3 minutes
    (120000, "That is a short song."),       # 2 minutes
])
def test_song_how_long(duration_ms, expected):
    """Test Song.how_long method for different durations"""
    song = Song(
        id=MOCK_SONG['id'],
        title=MOCK_SONG['name'],
        release_year=MOCK_SONG['album']['release_date'],
        href=MOCK_SONG['external_urls']['spotify'],
        explicit=MOCK_SONG['explicit'],
        duration_ms=duration_ms,
        disc_number=MOCK_SONG['disc_number'],
        popularity=MOCK_SONG['popularity']
    )
    assert song.how_long() == expected


def test_song_repr():
    """Test Song.__repr__ method"""
    song = Song(
        id=MOCK_SONG['id'],
        title=MOCK_SONG['name'],
        release_year=MOCK_SONG['album']['release_date'],
        href=MOCK_SONG['external_urls']['spotify'],
        explicit=MOCK_SONG['explicit'],
        duration_ms=MOCK_SONG['duration_ms'],
        disc_number=MOCK_SONG['disc_number'],
        popularity=MOCK_SONG['popularity']
    )
    assert str(song) == 'Song: Test Song - 2020-01-01'


@patch('media_grabber.spotify.get_album')
@patch('media_grabber.spotify.get_track')
def test_media_with_spotify_api(mock_get_track, mock_get_album):
    """Test Media and Song with mocked Spotify API calls"""
    mock_get_album.return_value = MOCK_ALBUM
    mock_get_track.return_value = MOCK_SONG

    # Test Media with get_album
    album = mock_get_album('5BWl0bB1q0TqyFmkBEupZy')
    media = Media(
        album['id'],
        album['name'],
        album['release_date'],
        album['external_urls']['spotify']
    )
    assert media.title == 'Test Album'
    assert media.summary().startswith('"Test Album"')

    # Test Song with get_track
    track = mock_get_track('75FEaRjZTKLhTrFGsfMUXR')
    song = Song(
        track['id'],
        track['name'],
        track['album']['release_date'],
        track['external_urls']['spotify'],
        track['explicit'],
        track['duration_ms'],
        track['disc_number'],
        track['popularity']
    )
    assert song.title == 'Test Song'
    assert song.how_long() == 'That song is medium length'
