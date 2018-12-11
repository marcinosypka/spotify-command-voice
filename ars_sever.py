import os
import time
import subprocess

filename = "test.wav"
sleep_time = 2
file_timestamp = os.path.getmtime(filename)
while True:
   current_timestamp = os.path.getmtime(filename)
   if current_timestamp != file_timestamp:
       print("SENDING NEW PROBE TO VOICELAB")
       subprocess.call(["./clsclient","-P","8131","-p", "Bearer b229b09f9e0c7f26f7de46b1022b3760","-addr", "grpc://demo.voicelab.pl:7722","-w","test.wav"])
       file_timestamp = os.path.getmtime(filename) 
   time.sleep(sleep_time)
