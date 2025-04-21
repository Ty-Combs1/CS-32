
import spotipy
import random
from spotipy.oauth2 import SpotifyClientCredentials

def get_random_song_from_year(year, client_id, client_secret):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    results = sp.search(q=f'year:{year}', type='track', limit=50)
    tracks = results['tracks']['items']

    if not tracks:
        return "No songs found for that year."

    random_track = random.choice(tracks)
    return f"Random song from {year}: {random_track['name']} by {random_track['artists'][0]['name']}"

# Replace with your actual credentials and desired year
client_id = 'faaee62665df4b2580ec95ce3d08e2a5'
client_secret = '4aa2dca94f01440abd33079036fdd098'
year = random.randint(1950, 2025)

random_song = get_random_song_from_year(year, client_id, client_secret)
print(random_song)
