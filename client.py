import socket
import pyaudio



def callback(input_data, frame_count, time_info, flags):
    frames.append(input_data)
    s.sendall(input_data)
    return input_data, pyaudio.paContinue


#record
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
RECORD_SECONDS = 40

HOST = '192.168.8.104'    # The remote host
PORT = 50007              # The same port as used by the server
device_info = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

p = pyaudio.PyAudio()
device_info = p.get_device_info_by_index(4)
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index = device_info["index"],
                stream_callback=callback,
                as_loopback=True)

print("*recording")

frames = []

while(1):
    pass

print("*done recording")

stream.stop_stream()
stream.close()
p.terminate()
s.close()

print("*closed")