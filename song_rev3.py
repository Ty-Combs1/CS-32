import spotipy
import random
from spotipy.oauth2 import SpotifyClientCredentials

def get_random_songs_from_year(year, client_id, client_secret, num_songs=5):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
    results = sp.search(q=f'year:{year}', type='track', limit=50)
    tracks = results['tracks']['items']
    if not tracks:
        return []
    return random.sample(tracks, min(num_songs, len(tracks)))

def get_songs_by_artists(artists, client_id, client_secret, num_songs=5):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
    songs = []
    for artist in artists:
        results = sp.search(q=f'artist:"{artist}"', type='track', limit=10)
        tracks = results['tracks']['items']
        for track in tracks:
            if len(songs) < num_songs:
                songs.append(track)
            else:
                break
        if len(songs) >= num_songs:
            break
    return songs


client_id = 'faaee62665df4b2580ec95ce3d08e2a5'
client_secret = '4aa2dca94f01440abd33079036fdd098'
year = random.randint(1950, 2025)

# Step 1: Show 5 random songs
songs = get_random_songs_from_year(year, client_id, client_secret, num_songs=5)
if not songs:
    print(f"No songs found for year {year}.")
    exit()

print(f"Here are 5 random songs from {year}:")
liked_artists = set()
for idx, song in enumerate(songs, 1):
    name = song['name']
    artist = song['artists'][0]['name']
    print(f"{idx}. {name} by {artist}")
    like = input(f"Do you like this song? (Y/N): ").strip().lower()
    if like == 'y':
        liked_artists.add(artist)

# Step 2: Give 5 more songs based on user input
if liked_artists:
    print("\nYou liked some songs! Here are 5 more songs from those artists:")
    more_songs = get_songs_by_artists(list(liked_artists), client_id, client_secret, num_songs=5)
    if not more_songs:
        print("Couldn't find more songs from those artists. Here are 5 more random songs:")
        more_songs = get_random_songs_from_year(year, client_id, client_secret, num_songs=5)
else:
    print("\nYou didn't like any songs. Here are 5 more random songs from the same year:")
    more_songs = get_random_songs_from_year(year, client_id, client_secret, num_songs=5)

for idx, song in enumerate(more_songs, 1):
    name = song['name']
    artist = song['artists'][0]['name']
    print(f"{idx}. {name} by {artist}")
