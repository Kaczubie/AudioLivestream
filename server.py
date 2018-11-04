import socket
import pyaudio
import wave
import subprocess


def set_master_volume(volume):
    val = float(int(volume))
    proc = subprocess.Popen('/usr/bin/amixer sset Master ' + str(val) + '%', shell=True, stdout=subprocess.PIPE)  #set volume on unix device
    proc.wait()


CHUNK = 4096  #same value as set on client 
FORMAT = pyaudio.paInt16 #same value as set on client 
CHANNELS = 2  #same value as set on client 
RATE = 48000  #same value as set on client 
RECORD_SECONDS = 40
WAVE_OUTPUT_FILENAME = "server_output.wav"
WIDTH = 2
frames = []

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 50007  # Port for audio data  Arbitrary non-privileged port
PORT2 = 50008  #Port for volume control. Both PORT and PORT2 should be set same on client and server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
v = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
v.bind((HOST, PORT2))

s.listen(1)
v.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
conn2, addr2 = v.accept()
conn2.setblocking(0)  #doesnt block when volume info is not available
print('super dziala', addr2)
data = conn.recv(4096)

i = 1

while data != '':

    stream.write(data)
    data = conn.recv(4096)
    i = i + 1
    print(i)
    frames.append(data)
    if i == 40:  #checking for volume data less often than getting audio data. Checking for volume info only when audio data present. 
        try:
            data2 = conn2.recv(2)    #exceptions appear when data not available 
        except socket.timeout as err:
            print("timeout")
        except socket.error as err:
            print("error")
        else:
            volume = data2.decode('utf8')
            set_master_volume(int(volume))
        i = 0

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

stream.stop_stream()
stream.close()
p.terminate()
conn.close()
conn2.close()




