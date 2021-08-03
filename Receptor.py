"""
Implements a client on one side to help listen for the server.
"""

import socket
from Fletcher import Fletcher
import pickle
import os
os.system('cls') if os.name == 'nt' else os.system('clear')
# DEPRECATED. Header size. Determines the size of the headers of a message.
HEADERSIZE = 10

# Connect the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 3001))

# Receive the message
full_msg = s.recv(4096)
data = pickle.loads(full_msg)
data = data.tobytes()
previous_checksum = input('Your previous checksum:\n>>> ').upper()

try:
    # Try to grab the checksum from the user, as if they were downloading a torrent, and check if they are both the same
    message_checksum = str(hex(Fletcher(data.decode('utf-8')).get_fletcher().result))[2:].upper()
    print(f'The message {data} is {f"not corrupted ({previous_checksum} == {message_checksum})" if previous_checksum == message_checksum else f"corrupted ({previous_checksum} != {message_checksum})"}!')
except:
    # If the message is too corrupt, then the UTF-8 decode will fail. Show the message using pure bytes instead, taking
    # advantage of Python's byte-sized reading.
    print('THIS MESSAGE IS TOO CORRUPT. EITHER CONTINUATION OR STARTING BYTES ARE UNSALVAGEABLE.')
    print('PREVIOUS MESSAGE DATA IS \033[93m\n\n\n', data, '\033[0m')


