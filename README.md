# spotify-command-voice
**ars-server.py**
 * if file test.wav changes sends request to voiclab api

**Python spotify lib**
   * pip install spotipy

**SpotifyWithPlayer python class**
* adds Spotify Player api support to spotipy.Spotify class

**Audio recording**

To stream audio from android IP Webcam can be used.
To capture audio stream on desktop open VLC media player, go to:

Media->Open Network Stream 
  
and enter stream url. Don't forget to select show more options and set caching to 1ms. Now you can use software like AudioRecorder to record audio from vlc.

To use sentence/command analysis Docker image from https://hub.docker.com/r/apohllo/krnnt/ needs to be run on your local machine.