"""
This helps launch the server. If you want to launch the receiver, run
    python Receptor.py
instead
"""

from Emisor import Server


# Instantiate the server
server = Server(port=3001, probability=0.01, with_checksum=True)

# Run the server
server.run()
