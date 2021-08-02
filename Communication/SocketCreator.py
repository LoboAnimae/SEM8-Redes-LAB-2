import socket


class SocketGenerator:
    def __init__(self):
        self.s = None

    def generate_socket(self, family=socket.AF_INET, stream=socket.SOCK_STREAM):
        self.s = socket.socket(family, stream)
        return self

    def accept(self):
        return self.s.accept()

    def bind(self, ip=socket.gethostname(), port=3000):
        self.s.bind((ip, port))
        return self

    def set_queue(self, new_queue):
        self.s.listen(new_queue)
        return self

    def close_socket(self):
        self.s.close()
