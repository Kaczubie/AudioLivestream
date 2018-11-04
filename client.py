import socket
import pyaudio
import struct



def callback(input_data, frame_count, time_info, flags):  # audio sent only when available, silence ignored thanks to using callback
    frames.append(input_data)
    s.sendall(input_data)
    return input_data, pyaudio.paContinue


#record
CHUNK = 4096   # big value here like 4096 may reduce lattency problem. in slow networks audio compression  may be needed -> may be added in next commits
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000    # RATE  and CHANNEL are device-dependent -> may be taken from device_info in next commits
RECORD_SECONDS = 40    

HOST = '192.168.0.22'    # The remote host
PORT = 50007              # Port for audio data
device_info = {}
PORT2 = 50008              #Port for volume control. Both PORT and PORT2 should be set same on client and server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
v = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
v.connect((HOST, PORT2))


p = pyaudio.PyAudio()
device_info = p.get_device_info_by_index(4)  # in my case device_id = 4 is WASAPI output
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index = device_info["index"],
                stream_callback=callback,  #gets soundcard output sound without using any microphone
                as_loopback=True)

print("*recording")

frames = []

while(1):

    vol_input = input("change volume?")
    v.sendall(bytes(str(vol_input), 'utf8'))  #whenever hit enter new volume value send to UNIX device runnig server and being set. If server is running on Windows device it wont work

print("*done recording")

stream.stop_stream()
stream.close()
p.terminate()
s.close()

print("*closed")