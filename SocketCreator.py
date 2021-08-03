"""
Quality of Life improvement for socket managment.
Main goal is to work like chaining functions from
Javascript.

Requires the socket library to work.
"""
import socket


class SocketGenerator:
    """
    Socket generator. Does not require anything to start itself.
    """
    def __init__(self):
        self.s = None

    def generate_socket(self, family: type(socket.AF_INET), stream: type(socket.SOCK_STREAM)):
        """
        Generates a new socket using a family and a stream

        :param family: Either a family or AF_INET
        :param stream: Either a stream or SOCK_STREAM
        :return:
        """
        self.s = socket.socket(family or socket.AF_INET, stream or socket.SOCK_STREAM)
        return self

    def accept(self):
        """
        Interface for the accept method from the socket

        :return: the accept function for the socket
        """
        return self.s.accept()

    def bind(self, ip: type(socket.AF_INET), port: int):
        """
        Binds the socket to an ip and a port.

        :param ip: The ip or the hostname
        :param port: The port or 3000
        :return: Itself
        """
        self.s.bind((ip or socket.gethostname(), port or 3000))
        return self

    def set_queue(self, new_queue: int):
        """
        Creates a queue of how many connections might be accepted before dropping one

        :param new_queue: The size of the queue
        :return: Itself
        """
        self.s.listen(new_queue)
        return self

    def close_socket(self):
        """
        Closes the socket

        :return: Itself
        """
        self.s.close()
