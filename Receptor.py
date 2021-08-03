import socket
from Fletcher import Fletcher
import pickle
import sys, os
os.system('cls') if os.name == 'nt' else os.system('clear')
HEADERSIZE = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 3001))

full_msg = s.recv(4096)
data = pickle.loads(full_msg)
data = data.tobytes()
previous_checksum = input('Your previous checksum:\n>>> ').upper()

try:
    message_checksum = str(hex(Fletcher(data.decode('utf-8')).get_fletcher().result))[2:].upper()
    print(f'The message {data} is {f"not corrupted ({previous_checksum} == {message_checksum})" if previous_checksum == message_checksum else f"corrupted ({previous_checksum} != {message_checksum})"}!')
except:
    print('THIS MESSAGE IS TOO CORRUPT. EITHER CONTINUATION OR STARTING BYTES ARE UNSALVAGEABLE.')
    print('PREVIOUS MESSAGE DATA IS \033[93m\n\n\n', data, '\033[0m')


