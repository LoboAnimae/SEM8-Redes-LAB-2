from Emisor import Server

server = Server(port=3001, probability=0.01, with_checksum = True)
server.run()
