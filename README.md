hello!! to make this work you have to make a .env file it's contents should be like this:

CLIENT_ID="your client id"
CLIENT_SECRET="your client secret"
REDIRECT_URI="your redirect uri"
PLAYLIST_ID="your spotify playlist id"

you'll also need to run:
'pip install ytmusicapi'
'pip install spotipy'
'pip install dotenv'

after that u simply run 'ytmusicapi oauth' and it should creat a 'oauth.json' file 

you can also set the offset in the track-count.txt to ur desire, if u want to start from the beginning of the spotify playlist
just leave it as it is.

then you should just be able to run the handleYT.py file and it should work just fine
