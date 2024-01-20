import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify client ID and secret ID
client_id = 'your_client_id'
client_secret = 'your_client_secret'
redirect_uri = 'your_redirect_uri' # The redirect URI that you set up on your Spotify developer dashboard

# Create a client credentials manager
client_credentials_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='playlist-modify-public')

# Create a Spotipy client
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Read the track links from the tracks.txt file
with open('tracks.txt', 'r') as f:
    track_links = [line.strip() for line in f.readlines()]

# Divide the track links into groups of 11000
chunk_size = 11000
track_chunks = [track_links[i:i+chunk_size] for i in range(0, len(track_links), chunk_size)]

# Create a playlist for each track chunk
for i, chunk in enumerate(track_chunks):
    start_track = i * chunk_size + 1
    end_track = (i+1) * chunk_size
    track_scope = f'{start_track}-{end_track}'
    playlist_name = f'Last.Fm ({track_scope})'
    playlist = sp.user_playlist_create(user='your_username', name=playlist_name, public=True)

    # Add the tracks to the playlist in groups of 100
    for j in range(0, len(chunk), 100):
        track_chunk = chunk[j:j+100]
        sp.user_playlist_add_tracks(user='your_username', playlist_id=playlist['id'], tracks=track_chunk)
