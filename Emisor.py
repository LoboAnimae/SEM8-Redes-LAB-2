"""
Class that helps create a virtual server based on sockets.
Requires the following libraries:
    random
    pickle
    bitarray

"""

import random
import pickle

from bitarray import bitarray

from SocketCreator import SocketGenerator
from Fletcher import Fletcher
from Hamming import Hamming


types = [ Fletcher, Hamming ]


def get_probability( probability: float, cast, based_hundred: bool = False ) -> float:
    """
    Gets the probability based on the cast.

    :param probability: The probability. Float.
    :param cast: int or float casters.
    :param based_hundred: Bool.
    :return: Takes the higher limit as a 100 or not
    """
    return cast( probability ) * (0.01 if based_hundred else 1)


def type_checker( variable, types_array: list ) -> None:
    """
    Checks the type of a variable to make sure it is one of the accepted types

    :param variable: The variable to be checked
    :param types_array: A list with the type constructors desired
    :return: None
    :raises: Exception if the correct type is not found
    """
    if type( variable ) not in types_array:
        raise Exception( f'{variable} is not the correct type! (Should be {types_array})' )


def enviar_cadena() -> str:
    """
    Grabs an input string. Made static. Previously in class.

    :return: The input string
    """
    return input( 'Your message:\n>>> ' ) or 'Default Message'


def enviar_objeto( directed_socket, message ) -> None:
    """
    Sends something through a Socket

    :param directed_socket: The socket
    :param message: The message to be sent
    :return: None
    """
    directed_socket.send( message )


class Server:
    """
    Server class that helps with the management of the server.
    """
    def __init__( self, encoding = 'utf8', noise_minmax = (0, 10000), probability = 0.01, based_hundred = False,
                  ip = None, port = 3000, socket_family = None, socket_stream = None, with_checksum = True ) -> None:
        """
        Initializer for the Server. All parameters are optional.

        :param encoding: The encoding. Defaults to 'utf8'
        :param noise_minmax: The noise to be used. It uses some math to detect the necessary chances. Tuple (min, max)
        :param probability: The probability that something will corrupt. Uses the noise_minmax to calculate itself.
        :param based_hundred: Whether the probability is based on 0-1 or 0-100. Defaults to False.
        :param ip: The ip to be used in the socket. Defaults to localhost.
        :param port: The port for the socket. Defaults to 3000
        :param socket_family: The socket family for the socket. Change only if the default does not work for you
        :param socket_stream: The socket stream method. Default is streaming. Should work correctly.
        :param with_checksum: Whether you want the checksum to be calculated or not, and then shown it.
        """
        type_checker( probability, [ str, int, float ] )
        type_checker( noise_minmax, [ list, tuple ] )
        type_checker( port, [ int ] )
        type_checker( based_hundred, [ bool ] )

        if type( probability ) is str:
            if '.' in probability:
                self.probability = get_probability( probability, float, based_hundred )
            else:
                self.probability = get_probability( probability, int, based_hundred )
        else:
            self.probability = get_probability( probability, type( probability ), based_hundred )

        # A simple Socket that stores a Socket class to make communication modular.
        self.socket = SocketGenerator().generate_socket( socket_family, socket_stream ).bind( ip, port ).set_queue( 5 )
        # The message to be broadcasted
        self.msg = ''
        # The minimum and maximum ranges
        self.MIN_RANGE, self.MAX_RANGE = noise_minmax
        # The encoding
        self.ENCODING = encoding
        # Object Checksum
        self.checksum = None
        # Whether we will calculate the checksum or not later on
        self.with_checksum = with_checksum

    def run( self )-> None:
        """
        Starts the server

        :return: None
        """
        # While we can, run the server
        while True:
            if not self.msg:
                # If the message is not set, set it
                print( 'Message not set.' )
                self.set_msg()
            client_socket = None
            # Declare the client_socket in the outer scope
            try:
                while True:
                    # Create a new loop inside so that we can actually interrupt the process and change the message
                    try:
                        # Accept a connection
                        client_socket, address = self.socket.accept()
                        # Notify the server-watcher
                        print( f'New connection from {address}. Sending message.' )
                        # Send the client a new "Corrupted" message
                        enviar_objeto( client_socket, self.msg )
                    except KeyboardInterrupt:
                        # If a keyboard interrupt happens, interrupt the process and attempt to reset the message. Treat
                        # as if it was the first time it ran
                        self.msg = ''
                        break
                    finally:
                        # Close the socket, no matter what
                        client_socket.close()
            except KeyboardInterrupt:
                # Buggy outside keyboardinterrupt. Resets the message and closes the socket.
                self.msg = ''
                if client_socket is not None:
                    client_socket.close()

    def set_msg( self ) -> None:
        """
        Sets the message through a conveyor-belt-like process.

        :return: None
        """
        # Set the message to an input
        new_message = enviar_cadena()
        # If the user wants a checksum, grab it and
        if self.with_checksum:
            checksum = Fletcher( new_message ).get_fletcher().result
            print( f'Checksum 32 for you message: {str( hex( checksum ) )[ 2: ].upper()}' )
        bit_arr = self.enviar_cadena_segura( new_message )
        self.agregar_ruido( bit_arr )
        self.msg = pickle.dumps( bit_arr )
        return None

    def msg_set( self ):
        return bool( self.msg )

    def enviar_cadena_segura( self, message: str ) -> type( bitarray ):
        a = bitarray()
        a.frombytes( bytes( message, self.ENCODING ) )
        return a

    def agregar_ruido( self, pure_bitarray ) -> None:
        corrupted_at_least_once = False
        corrupted_bits = 0
        while not corrupted_at_least_once:
            for index, bit in enumerate( pure_bitarray ):
                chance = random.randint( self.MIN_RANGE, self.MAX_RANGE )
                if chance <= self.MAX_RANGE * self.probability:
                    corrupted_bits += 1
                    corrupted_at_least_once = True
                    pure_bitarray[ index ] = not pure_bitarray[ index ]
        print( f'Corrupted a total {corrupted_bits} bits' )
        print( f'New message is {pure_bitarray.tobytes()}' )

# Made with help of
# https://www.electrically4u.com/hamming-code-with-a-solved-problem/#:~:text=The%20hamming%20code%20uses%20the,information%20bits%20in%20the%20message.&text=For%20example%2C%20if%204%2Dbit,the%20trial%20and%20error%20method.&text=The%20above%20equation%20implies%204%20not%20greater%20than%20or%20equal%20to%207.
