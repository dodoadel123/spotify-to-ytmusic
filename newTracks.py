import spotipy
from spotipy import SpotifyOAuth
from dotenv import load_dotenv
import numpy as np
import os

load_dotenv()

class tracks:
    def __init__(self):
        #enviroment variables
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.redirect_URI = os.getenv("REDIRECT_URI")
        self.playlist_id = os.getenv("PLAYLIST_ID") 
        
        #request variables
        self.scope = "playlist-modify-public"
        self.new_offset = -1 #make it any unique number that won't be reached normally in the program
        
        #response variables (use these to search for the songs in YTmusic)
        self.trackNames = []
        self.artists = []
        self.albums = []
        self.SPdurations_Ms = [] #duration of the song in milli seconds
        self.SPdurations_Min = [] #duration of the song in minutes (i.e 3:22)
        self.SPdurations_Min_Plus = [] #duration of the song in minutes but plus a second (i.e 3:23)
        self.SPdurations_Min_Minus = [] #duration of the song in minutes but minus a second (i.e 3:21)
        
        #defining the offset that is read from the file
        with open('track-count.txt', 'r+') as file:
            self.offset = int(file.read())    
            
    def spotipyRequest(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
                                               client_secret=self.client_secret,
                                               redirect_uri=self.redirect_URI,
                                               state=None,
                                               scope=self.scope))
        
        self.userTracks = self.sp.playlist_tracks(playlist_id=self.playlist_id,
                                                  fields=None,
                                                  limit=100,
                                                  offset=self.offset)
        
        return self.userTracks #returning spotify's response 
    
    def msTOmin(self):
        for x in range(0, len(self.SPdurations_Ms)):
            #convert milli seconds to minutes
            durationMS = self.SPdurations_Ms[x]
            durationMin = str((int(durationMS) / (10 * 10 * 10)) / 60)
            
            #converting the the decimals into seconds and then rounding it to the nearest number
            Sec_decimals = float(durationMin) - int(durationMin[0])
            seconds = int(np.round(Sec_decimals * 60))
            seconds_Plus = seconds + 1
            seconds_Minus = seconds - 1
            
            if seconds < 10 :
                self.SPdurations_Min.append(f'{durationMin[0]}:0{seconds}')
                            
            if seconds_Minus < 10:
                if seconds == 0:
                    seconds_Minus = 59
                    self.SPdurations_Min_Minus.append(f'{int(durationMin[0]) - 1}:{seconds_Minus}')
                else:     
                    self.SPdurations_Min_Minus.append(f'{durationMin[0]}:0{seconds_Minus}')
                
            if seconds_Plus < 10:
                self.SPdurations_Min_Plus.append(f'{durationMin[0]}:0{seconds_Plus}')
            
            if seconds >= 10:    
                self.SPdurations_Min.append(f'{durationMin[0]}:{seconds}')
                
            if seconds_Minus >= 10 and seconds_Minus != 59:    
                self.SPdurations_Min_Minus.append(f'{durationMin[0]}:{seconds_Minus}')
                
            if seconds_Plus >= 10:
                if seconds == 59:
                    seconds_Plus = 0
                    self.SPdurations_Min_Plus.append(f'{int(durationMin[0])+ 1}:0{seconds_Plus}')
                else:
                    self.SPdurations_Min_Plus.append(f'{durationMin[0]}:{seconds_Plus}')
            
    def handleResp(self):
        for idx, item in enumerate(self.spotipyRequest()['items']):
            self.track = item['track']
            self.new_offset  = idx + int(self.offset) + 1
            
            self.artists.append(self.track['artists'][0]['name']) #array of the names of the artists of the added songs
            self.trackNames.append(self.track['name']) #array of the names of the added songs
            self.albums.append(self.track['album']['name']) #array of the names of albums of the added songs
            self.SPdurations_Ms.append(self.track['duration_ms']) #array of the durations of each song in milli seconds
            
        self.changeOffset() #--> to change to the new offset right after we check for new songs
        self.msTOmin()
            
    def changeOffset(self):
        self.totalTracks = self.spotipyRequest()['total'] #total number of songs in the playlist
        
        with open('track-count.txt', 'r+') as file:
            if self.offset != self.new_offset and self.new_offset != -1:
                if self.new_offset == self.totalTracks:
                    #check if the current offset is equal to the total number of songs in the playlist
                    #if so it will write the current offset minus 5 to avoid breaking the program in case the user 
                    #decided to delete songs from the spotify playlist
                    file.write(str(self.new_offset - 5))
                else:    
                    file.write(str(self.new_offset))
            else:
                file.write(str(self.offset))

tracks = tracks()
response = tracks.handleResp()

