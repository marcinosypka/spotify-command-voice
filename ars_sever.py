import os
import time
import subprocess
from data.pattern import get_commands
import spotipy.util as util
from SpotifyWithPlayer import SpotifyWithPlayer

scope = 'user-modify-playback-state user-read-currently-playing user-read-playback-state'
username = '26yuotyu35tiipythyrrs7jox04v5'
client_id = '9c862d0167b04dcd9ae3de8fc25d509b'
client_secret = '6a7729412eb442b794b5ce623beca996'
redirect_uri = 'http://localhost.com'
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
print("token obtained")
print("the token is: " + token)
sp = SpotifyWithPlayer(auth=token)
volume = 50
shuffle = False
repeat_states = ['track', 'context', 'off']
current_repeat_state = 0
sp.current_user_volume(volume)
def increase_volume(volume):
    if volume < 100:
        volume = volume + 5
    return volume


def decrease_volume(volume):
    if volume > 0:
        volume = volume - 5
    return volume

filename = "test.wav"
sleep_time = 2
file_timestamp = os.path.getmtime(filename)
while True:
   current_timestamp = os.path.getmtime(filename)
   if current_timestamp != file_timestamp:
       print("SENDING NEW PROBE TO VOICELAB")
       result = subprocess.check_output(["./clsclient","-P","8131","-p", "Bearer b229b09f9e0c7f26f7de46b1022b3760","-addr", "grpc://demo.voicelab.pl:7722","-w","test.wav"])
       command = result.decode('utf-8').split('\n')[0]
       print(command)
       spotify_command = get_commands(command, 'data/updated_results_manual.txt')
       print(spotify_command)
       if 'STOP' in spotify_command:
           sp.current_user_pause()
       elif 'START' in spotify_command:
           sp.current_user_play()
       elif 'BACK' in spotify_command:
           sp.current_user_previous()
       elif 'NEXT' in spotify_command:
           sp.current_user_next()
       elif 'VOLUME_UP' in spotify_command:
           volume = increase_volume(volume)
           sp.current_user_volume(volume)
       elif 'VOLUME_DOWN' in spotify_command:
           volume = decrease_volume(volume)
           sp.current_user_volume(volume)
       elif 'SHUFFLE' in spotify_command:
           sp.current_user_shuffle(shuffle)
           shuffle = not shuffle
       elif 'LOOP' in spotify_command:
           sp.current_user_repeat(repeat_states[current_repeat_state])
           print(current_repeat_state)
           current_repeat_state = (current_repeat_state + 1) % 3

       file_timestamp = os.path.getmtime(filename)
   time.sleep(sleep_time)
