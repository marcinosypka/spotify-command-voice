from SpotifyWithPlayer import SpotifyWithPlayer
import spotipy.util as util


scope = 'user-modify-playback-state user-read-currently-playing user-read-playback-state'
username ='26yuotyu35tiipythyrrs7jox04v5'
client_id = '9c862d0167b04dcd9ae3de8fc25d509b'
client_secret = '6a7729412eb442b794b5ce623beca996'
redirect_uri = 'http://localhost.com'
token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)

sp = SpotifyWithPlayer(auth=token)
