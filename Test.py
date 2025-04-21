// Spotify Random Year Explorer
// A tool to discover top songs from a randomly selected year

const express = require('express');
const axios = require('axios');
const SpotifyWebApi = require('spotify-web-api-node');
require('dotenv').config();

const app = express();
const port = 3000;

// Serve static files
app.use(express.static('public'));
app.use(express.json());

// Initialize Spotify API client
const spotifyApi = new SpotifyWebApi({
  clientId: process.env.SPOTIFY_CLIENT_ID,
  clientSecret: process.env.SPOTIFY_CLIENT_SECRET,
  redirectUri: `http://localhost:${port}/callback`
});

// Routes
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

// Login route
app.get('/login', (req, res) => {
  const scopes = ['user-read-private', 'user-read-email'];
  const authorizeURL = spotifyApi.createAuthorizeURL(scopes);
  res.redirect(authorizeURL);
});

// Callback route after Spotify login
app.get('/callback', async (req, res) => {
  const { code } = req.query;

  try {
    const data = await spotifyApi.authorizationCodeGrant(code);
    spotifyApi.setAccessToken(data.body['access_token']);
    spotifyApi.setRefreshToken(data.body['refresh_token']);

    res.redirect('/');
  } catch (error) {
    console.error('Error during authorization:', error);
    res.status(500).send('Authorization failed');
  }
});

// API endpoint to get random year songs
app.get('/api/random-year-songs', async (req, res) => {
  try {
    // Get random year between 1950 and current year
    const currentYear = new Date().getFullYear();
    const minYear = 1950;
    const randomYear = Math.floor(Math.random() * (currentYear - minYear + 1)) + minYear;

    // Get access token (renew if needed)
    await ensureValidToken();

    // Get top tracks from that year
    const response = await axios.get('https://api.spotify.com/v1/search', {
      headers: {
        'Authorization': `Bearer ${spotifyApi.getAccessToken()}`
      },
      params: {
        q: `year:${randomYear}`,
        type: 'track',
        limit: 50,
        market: 'US'
      }
    });

    // Select 5 random tracks from the results
    const tracks = response.data.tracks.items;
    const selectedTracks = getRandomItems(tracks, 5);

    res.json({
      year: randomYear,
      tracks: selectedTracks.map(track => ({
        id: track.id,
        name: track.name,
        artist: track.artists.map(artist => artist.name).join(', '),
        album: track.album.name,
        releaseDate: track.album.release_date,
        previewUrl: track.preview_url,
        spotifyUrl: track.external_urls.spotify,
        albumCover: track.album.images[1]?.url
      }))
    });
  } catch (error) {
    console.error('Error fetching tracks:', error);
    res.status(500).json({ error: 'Failed to fetch tracks' });
  }
});

// Helper function to ensure we have a valid token
async function ensureValidToken() {
  try {
    const data = await spotifyApi.refreshAccessToken();
    spotifyApi.setAccessToken(data.body['access_token']);
  } catch (error) {
    console.error('Error refreshing token:', error);
  }
}

// Helper function to get random items from an array
function getRandomItems(array, count) {
  const shuffled = [...array].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
}

// Start server
app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
});
