hello!! to make this work you have to make a .env file it's contents should be like this:

CLIENT_ID="your client id"
CLIENT_SECRET="your client secret"
REDIRECT_URI="your redirect uri"
PLAYLIST_ID="your spotify playlist id"

you'll need to run 'pip install ytmusicapi' in the terminal to install the yt music api that i use here
after that u simply run 'ytmusicapi oauth' and it should creat a 'oauth.json' file 

you can also set the offset in the track-count.txt to ur desire, if u want to start from the beginning of the spotify playlist
just leave it as it is, if you already have some songs in your yt music playlist just set the number to the last item's index

then you should just be able to run the handleYT.py file and it should work just fine
