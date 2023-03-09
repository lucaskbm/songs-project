#!/usr/bin/env python
# coding: utf-8

# # Installation & API connection & Libraries

# In[1]:


# Install Spotipy 
!pip install spotipy

# In[16]:


# Import libraries
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import os


import networkx as nx
import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns


# In[17]:


# Initiate with your credentials

client_id = '47020c3ba7b1404a938636c6a468a7b3'
client_secret = 'dc9c0f619b61431e85b00c8d34cb842d'

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


# In[18]:


# Playlist authentication setup

# Authentication with the URI required to add songs to a playlist
os.environ["SPOTIPY_CLIENT_ID"] = "47020c3ba7b1404a938636c6a468a7b3"
os.environ["SPOTIPY_CLIENT_SECRET"] = "dc9c0f619b61431e85b00c8d34cb842d"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8888/callback"

# Add your Spotify username
username = "lkenji.magalhaes"

# Scope refers to the permissions you're given
scope = "playlist-modify-public"
token = util.prompt_for_user_token(username, scope)
sp = spotipy.Spotify(auth=token)


# In[39]:


# Test the connection
this_house = sp.search(q='track:"We built this house" artist:"Scorpions"', type='track')
crazy = sp.search(q='track:"Crazy" artist:"Aerosmith"', type='track')
print(crazy)


# # Exploring Similar Songs

# In[40]:


# Get features for first song: "We built this house" - Scorpions
this_house_id = this_house['tracks']['items'][0]['id']
this_house_features = sp.audio_features(this_house_id)[0]
print(this_house_features)

# Get features for second song: "Sometime I feel like screaming" - Deep Purple
crazy_id = crazy['tracks']['items'][0]['id']
crazy_features = sp.audio_features(crazy_id)[0]
print(crazy_features)


# In[26]:


# Get the audio features for "We Built This House"
track_uri = this_house['tracks']['items'][0]['uri']
track_features = sp.audio_features(track_uri)[0]

# Define the features to use for similarity comparison (from Spotify API)
similar_features = ['danceability', 'energy', 'acousticness', 'instrumentalness', 'valence', 'loudness', 'tempo']

# Create a DataFrame to store the similar songs
similar_song1 = pd.DataFrame(columns=['title', 'artist', 'album', 'release_date', 'uri'] + similar_features)

# Search for tracks similar to "We Built This House" and add them to the DataFrame
results = sp.recommendations(seed_artists=None, seed_tracks=[track_uri], seed_genres=None, limit=20)
for track in results['tracks']:
    track_uri = track['uri']
    track_features = sp.audio_features(track_uri)[0]
    track_info = [track['name'], track['artists'][0]['name'], track['album']['name'], track['album']['release_date'], track_uri]
    similar_song1.loc[len(similar_song1)] = track_info + [track_features[feat] for feat in similar_features]

print(similar_song1)


# In[41]:


# Get features for "Sometime I feel like screaming"
crazy_id = feel_like_scream['tracks']['items'][0]['id']
crazy_features = sp.audio_features(feel_like_scream_id)[0]

# Define the features to use for similarity comparison (from Spotify API)
similar_features = ['danceability', 'energy', 'acousticness', 'instrumentalness', 'valence', 'loudness', 'tempo']

# Create a DataFrame to store the similar songs
similar_song2 = pd.DataFrame(columns=['title', 'artist', 'album', 'release_date', 'uri'] + similar_features)

# Search for tracks similar to "We Built This House" and add them to the DataFrame
results = sp.recommendations(seed_artists=None, seed_tracks=[track_uri], seed_genres=None, limit=20)
for track in results['tracks']:
    track_uri = track['uri']
    track_features = sp.audio_features(track_uri)[0]
    track_info = [track['name'], track['artists'][0]['name'], track['album']['name'], track['album']['release_date'], track_uri]
    similar_song2.loc[len(similar_song2)] = track_info + [track_features[feat] for feat in similar_features]

print(similar_song2)


# ## Add the songs to a new Spotify Playlist

# In[42]:


# Create a new playlist
playlist_name = "Next Trip"
playlist_description = "A playlist for our next trip created using Spotify API"
playlist = sp.user_playlist_create(user=sp.current_user()['id'], name=playlist_name, public=True, description=playlist_description)

# Add the similar songs to the playlist
track_uris = similar_song1['uri'].tolist() + similar_song2['uri'].tolist()
sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)


# # Exploring Similar Bands

# In[29]:


# Get the artist URI for "We Built This House"
artist_uri = this_house['tracks']['items'][0]['artists'][0]['uri']

related_artists_scorpions = sp.artist_related_artists(artist_uri)["artists"]

G = nx.Graph()
G.add_node("Scorpions")
for artist in related_artists_scorpions:
    name = artist["name"]
    G.add_node(name)
    G.add_edge("Scorpions", name)

pos = nx.spring_layout(G, k=0.2)
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=8, font_weight="bold")
plt.show()


# In[52]:


# Get the artist URI for "Sometimes I Feel Like Screaming"
artist_uri = feel_like_scream['tracks']['items'][0]['artists'][0]['uri']

related_artists_purple = sp.artist_related_artists(artist_uri)["artists"]

G = nx.Graph()
G.add_node("Aerosmith")
for artist in related_artists_purple:
    name = artist["name"]
    G.add_node(name)
    G.add_edge("Aerosmith", name)

pos = nx.spring_layout(G, k=0.2)
nx.draw(G, pos, with_labels=True, node_color="lightgreen", node_size=800, font_size=8, font_weight="bold")
plt.show()


# In[64]:


# Get the artist URI for "We Built This House"
artist_uri = this_house['tracks']['items'][0]['artists'][0]['uri']

related_artists_scorpions = sp.artist_related_artists(artist_uri)["artists"]

# Get the artist URI for "Sometimes I Feel Like Screaming"
artist_uri = crazy['tracks']['items'][0]['artists'][0]['uri']

related_artists_aero = sp.artist_related_artists(artist_uri)["artists"]

G = nx.Graph()

# Add Scorpions related artists to the graph
G.add_node("Scorpions")
for artist in related_artists_scorpions:
    name = artist["name"]
    G.add_node(name)
    G.add_edge("Scorpions", name)

# Add Deep Purple related artists to the graph
G.add_node("Aerosmith")
for artist in related_artists_aero:
    name = artist["name"]
    G.add_node(name)
    G.add_edge("Aerosith", name)

# Find the intersection between the two sets of related artists
intersection = set([a["name"] for a in related_artists_scorpions]).intersection(set([a["name"] for a in related_artists_aero]))

# Add the intersection nodes to the graph and connect them to their corresponding artists
for artist in related_artists_scorpions:
    if artist["name"] in intersection:
        name = artist["name"]
        G.add_node(name)
        G.add_edge("Scorpions", name)
for artist in related_artists_aero:
    if artist["name"] in intersection:
        name = artist["name"]
        G.add_node(name)
        G.add_edge("Aerosmith", name)

pos = nx.spring_layout(G, k=0.2)
nx.draw(G, pos, with_labels=True, node_size=300, font_size=8, font_weight="light")
plt.show()


# In[49]:


# Get the playlist ID for "Trip"
playlist_name = "Next Trip"
playlists = sp.user_playlists(sp.current_user()['id'])
playlist_id = None
for playlist in playlists['items']:
    if playlist['name'] == playlist_name:
        playlist_id = playlist['id']
        break

# Get the top 2 songs from the related artists
top_songs = []
for artist in related_artists_scorpions:
    artist_uri = artist['uri']
    top_tracks = sp.artist_top_tracks(artist_uri)['tracks'][:2]
    top_songs.extend(top_tracks)
    
for artist in related_artists_aero:
    artist_uri = artist['uri']
    top_tracks = sp.artist_top_tracks(artist_uri)['tracks'][:2]
    top_songs.extend(top_tracks)

# Add the top 2 songs to the playlist
track_uris = [song['uri'] for song in top_songs]
sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)


# In[50]:


# Define a list of artists to analyze
artists = ["Scorpions"]
artists.extend([artist["name"] for artist in sp.artist_related_artists(artist_uri)["artists"]])

# Define a list of features to analyze
features = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]

# Create an empty DataFrame to store the features for each artist
df = pd.DataFrame(columns=["artist"] + features)

# Iterate over the artists and retrieve their features
for artist in artists:
    tracks = sp.artist_top_tracks(sp.search(artist, type="artist")["artists"]["items"][0]["uri"])["tracks"]
    features_list = []
    for track in tracks:
        track_uri = track["uri"]
        track_features = sp.audio_features(track_uri)[0]
        features_list.append([track_features.get(feat) for feat in features])
    artist_features = [artist] + [sum(x)/len(x) for x in zip(*features_list)]
    df.loc[len(df)] = artist_features

# Print the DataFrame
print(df)

# Create a heatmap of the correlation matrix
corr = df[features].corr()
fig, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(corr, cmap="coolwarm", annot=True, square=True)
plt.show()


# # Asking for user's input

# In[ ]:


sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id = client_id, client_secret = client_secret, 
                                       scope = 'playlist-read-private user-modify-playback-state')


# In[ ]:


import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class PlaylistGenerator(QWidget):
    def __init__(self):
        super().__init__()

        # Set up GUI
        self.setWindowTitle("Playlist Generator")
        self.button_layout = QVBoxLayout()

        # Add mood buttons
        self.relax_button = QPushButton("Warley")
        self.relax_button.clicked.connect(lambda: self.play_playlist("Warley"))
        self.button_layout.addWidget(self.relax_button)

        self.rock_button = QPushButton("80's Rock n' Roll")
        self.rock_button.clicked.connect(lambda: self.play_playlist("80's Rock n' Roll"))
        self.button_layout.addWidget(self.rock_button)

        self.mpb_button = QPushButton("MPB")
        self.mpb_button.clicked.connect(lambda: self.play_playlist("MPB"))
        self.button_layout.addWidget(self.mpb_button)

        self.study_button = QPushButton("Study")
        self.study_button.clicked.connect(lambda: self.play_playlist("Study"))
        self.button_layout.addWidget(self.study_button)

        self.energy_button = QPushButton("Energy")
        self.energy_button.clicked.connect(lambda: self.play_playlist("Energy"))
        self.button_layout.addWidget(self.energy_button)

        self.setLayout(self.button_layout)
        self.show()

    def play_playlist(self, playlist_name):
        # Search for the playlist and get its ID
        playlists = sp.user_playlists(sp.current_user()['id'])
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
                break

        # Play the playlist in the Spotify app
        sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    generator = PlaylistGenerator()
    sys.exit(app.exec_())


# In[ ]:





# In[ ]:




