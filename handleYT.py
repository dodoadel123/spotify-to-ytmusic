from ytmusicapi import YTMusic
from newTracks import tracks

yt = YTMusic('D:\code\python\spotify\oauth.json')

playlistId = 'PLSliFNikKOx4bS8N9OnC4Fyv5wwm3khV9' 

trackNames = tracks.trackNames #list of track names from spotify
artistNames = tracks.artists #list of artists' names from spotify
albumNames = tracks.albums #list of album names from spotify
durations = tracks.SPdurations_Min #list of durations of the songs

def search(trackName, artistName, albumName):
     search_result = yt.search(f'{trackName} by {artistName}', filter='songs')
     return search_result

for x in range(0, len(trackNames)):
     track = trackNames[x]
     artist = artistNames[x]
     album = albumNames[x]
     duration = durations[x]
     
     for y in range(0, 5):
          if search(track, artist, album)[y]['title'] == track or search(track, artist, album)[y]['duration'] == duration or search(track, artist, album)[y]['duration'] == tracks.SPdurations_Min_Minus[x] or search(track, artist, album)[y]['duration'] == tracks.SPdurations_Min_Plus[x]:
               yt.add_playlist_items(playlistId=playlistId, videoIds=[search(track, artist, album)[y]['videoId']])
               break
          
     print(f'{x + 1} : {track} by {artist} - {album}                {duration}')
