import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv

# set up Spotify API credentials
client_id = 'your_client_id'
client_secret = 'your_client_secret'
redirect_uri = 'your_redirect_uri'

scope = "playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# create csv file and write headers
csv_file = open('spotify_playlists.csv', 'a', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file)
if os.path.exists('checkpoint.txt'):
    # if checkpoint file exists, read the last exported playlist index from it
    with open('checkpoint.txt', 'r') as f:
        playlist_index = int(f.read())
else:
    # otherwise, start from the first playlist
    playlist_index = 1
    csv_writer.writerow(['artist_id', 'track_id', 'album_id', 'artist_name', 'track_name', 'album_name', 'track_popularity', 'release_date', 'playlist_id', 'playlist_name', 'playlist_index'])

# get user's playlists
playlists = sp.current_user_playlists(limit=50, offset=(playlist_index - 1))

try:
    # iterate through each playlist
    while playlists:
        for playlist in playlists['items']:
            # get playlist tracks
            offset = 0
            while True:
                tracks = sp.playlist_tracks(playlist['id'], offset=offset)
                for track in tracks['items']:
                    # get track information
                    track_id = track['track']['id']
                    artist_id = track['track']['artists'][0]['id']
                    album_id = track['track']['album']['id']
                    artist_name = track['track']['artists'][0]['name']
                    track_name = track['track']['name']
                    album_name = track['track']['album']['name']
                    track_popularity = track['track']['popularity']
                    release_date = track['track']['album']['release_date']
                    playlist_id = playlist['id']
                    playlist_name = playlist['name']
                    # write track information to csv with playlist index
                    csv_writer.writerow([artist_id, track_id, album_id, artist_name, track_name, album_name, track_popularity, release_date, playlist_id, playlist_name, playlist_index])

                offset += len(tracks['items'])
                if not tracks['next']:
                    break
                    
            print(f"Playlist {playlist['name']} finished exporting")
            playlist_index += 1
            # update checkpoint file with last exported playlist index
            with open('checkpoint.txt', 'w') as f:
                f.write(str(playlist_index))
                
        playlists = sp.next(playlists)
        
except KeyboardInterrupt:
    # if the script is interrupted, update the checkpoint file with the last exported playlist index and exit gracefully
    with open('checkpoint.txt', 'w') as f:
        f.write(str(playlist_index))
    csv_file.close()
    exit(0)

# close csv file
csv_file.close()
# remove checkpoint file as all playlists have been exported
os.remove('checkpoint.txt')
