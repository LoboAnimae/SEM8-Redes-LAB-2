import socket


class SocketGenerator:
    def __init__(self):
        self.s = None

    def generate_socket(self, family, stream):
        self.s = socket.socket(family or socket.AF_INET, stream or socket.SOCK_STREAM)
        return self

    def accept(self):
        return self.s.accept()

    def bind(self, ip, port):
        self.s.bind((ip or socket.gethostname(), port or 3000))
        return self

    def set_queue(self, new_queue):
        self.s.listen(new_queue)
        return self

    def close_socket(self):
        self.s.close()
