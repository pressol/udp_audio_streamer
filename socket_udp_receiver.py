# socket_multicast_receiver.py
import socket
import struct
import sys
import zlib

import pyaudio

CHUNK = 256
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
BLOCK_SIZE = 16

UDP_IP = ""
UDP_PORT = 10000


# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind((UDP_IP, UDP_PORT))

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

# Receive/respond loop
reack=0
while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(2048)
    if reack == 0:
        print('received {} bytes from {}'.format(
            len(data), address))
        print(data)

        print('sending acknowledgement to', address)
        sock.sendto(b'ack', address)
        reack=1
    else:
        print('waiting for the stream data')
        data = zlib.decompress(data)
        stream.write(data)

stream.stop_stream()
stream.close()
p.terminate()
