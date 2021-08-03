import random
import pickle

from bitarray import bitarray

from SocketCreator import SocketGenerator
from Fletcher import Fletcher
from Hamming import Hamming

types = [Fletcher, Hamming]


def get_probability(probability, cast, based_hundred=False):
    return cast(probability) * (0.01 if based_hundred else 1)


def type_checker(variable, types) -> None:
    if type(variable) not in types:
        raise Exception(
            f'{variable} is not the correct type! (Should be {types})')


def enviar_cadena() -> str:
    return input('Your message:\n>>> ') or 'Default Message'


def enviar_objeto(directed_socket, message):
    directed_socket.send(message)


class Server:
    def __init__(self, encoding='utf8', noise_minmax=(0, 10000), probability=0.01, based_hundred=False,
                 ip=None, port=3000, socket_family=None, socket_stream=None, with_checksum=True):
        type_checker(probability, [str, int, float])
        type_checker(noise_minmax, [list, tuple])
        type_checker(port, [int])
        type_checker(based_hundred, [bool])

        if type(probability) is str:
            if '.' in probability:
                self.probability = get_probability(
                    probability, float, based_hundred)
            else:
                self.probability = get_probability(
                    probability, int, based_hundred)
        else:
            self.probability = get_probability(
                probability, type(probability), based_hundred)
        self.socket = SocketGenerator().generate_socket(
            socket_family, socket_stream).bind(ip, port).set_queue(5)
        self.msg = ''
        self.MIN_RANGE, self.MAX_RANGE = noise_minmax
        self.ENCODING = encoding
        self.checksum = None
        self.with_checksum = with_checksum

    def run(self):
        while True:
            if not self.msg:
                print('Message not set.')
                self.set_msg()
            client_socket = None
            try:
                while True:
                    try:
                        client_socket, address = self.socket.accept()
                        print(
                            f'New connection from {address}. Sending message.')
                        enviar_objeto(client_socket, self.msg)
                    except KeyboardInterrupt:
                        self.msg = ''
                        break
                    finally:
                        client_socket.close()
            except KeyboardInterrupt:
                self.msg = ''
                if client_socket is not None:
                    client_socket.close()

    def set_msg(self):
        new_message = enviar_cadena()
        if self.with_checksum:
            checksum = Fletcher(new_message).get_fletcher().result
            print(
                f'Checksum 32 for you message: {str(hex(checksum))[2:].upper()}')
        else:
            hamming = Hamming(new_message).implement_redundant_bits()
            print(
                f'Hamming 32 for you message: {str(hex(hamming))[2:].upper()}')

        bit_arr = self.enviar_cadena_segura(new_message)
        self.agregar_ruido(bit_arr)
        self.msg = pickle.dumps(bit_arr)
        return None

    def msg_set(self):
        return bool(self.msg)

    def enviar_cadena_segura(self, message: str) -> type(bitarray):
        a = bitarray()
        a.frombytes(bytes(message, self.ENCODING))
        return a

    def agregar_ruido(self, pure_bitarray) -> None:
        corrupted_at_least_once = False
        corrupted_bits = 0
        while not corrupted_at_least_once:
            for index, bit in enumerate(pure_bitarray):
                chance = random.randint(self.MIN_RANGE, self.MAX_RANGE)
                if chance <= self.MAX_RANGE * self.probability:
                    corrupted_bits += 1
                    corrupted_at_least_once = True
                    pure_bitarray[index] = not pure_bitarray[index]
        print(f'Corrupted a total {corrupted_bits} bits')
        print(f'New message is {pure_bitarray.tobytes()}')


# Made with help of
# https://www.electrically4u.com/hamming-code-with-a-solved-problem/#:~:text=The%20hamming%20code%20uses%20the,information%20bits%20in%20the%20message.&text=For%20example%2C%20if%204%2Dbit,the%20trial%20and%20error%20method.&text=The%20above%20equation%20implies%204%20not%20greater%20than%20or%20equal%20to%207.
