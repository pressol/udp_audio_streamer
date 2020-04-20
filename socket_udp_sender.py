#socket_multicast_sender.py
import socket
import struct
import sys
import zlib
import pyaudio

message = b'very important data'

UDP_IP = ""
UDP_PORT = 10000

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
sock.settimeout(1)

try:

    # Send data to the multicast group
    print('sending {!r}'.format(message))
    sent = sock.sendto(message, (UDP_IP, UDP_PORT))

    # Look for responses from all recipients
    responce = 0
    while True:
        if responce == 0:
            print('waiting to receive')
            try:
                data, server = sock.recvfrom(16)
            except socket.timeout:
                print('timed out, no more responses')
                break
            else:
                print('received {!r} from {}'.format(
                    data, server))
                responce = 1
        else:

            CHUNK = 256
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            BLOCK_SIZE = 16

            p = pyaudio.PyAudio()

            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

            print("* streaming")
            frames = []

            while True:
                data = stream.read(CHUNK)
                sent = sock.sendto(zlib.compress(data, 7), (UDP_IP, UDP_PORT))
                #sent = sock.sendto(data, (UDP_IP, UDP_PORT))

finally:
    print('closing socket')
    sock.close()
