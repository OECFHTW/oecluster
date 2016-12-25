#!/usr/bin/env python3

__version__ = "0.1"

# Author: Funny program style guy & friends

import socket
import sys

from util.config.logger import Log

# nico: writing to stderr is not the preferred way of user communication!!


# The Server class for TCP/IP communication
class Client:

    def __init__(self, server_address='localhost', port=20000):
        self._logger = Log.get_logger(self.__class__.__name__)
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.server_address = server_address
        self.port = port
        self.server = (server_address, port)


        # nico: you actually dont do what you print out - the connect function is not even called.
        self._logger.info('connecting to %s port %d', server_address, port)
        self._logger.info(sys.stderr, 'starting up on %s port %d', server_address, port)

    def connect(self):
        self.sock.connect(self.server)
        try:

            # Send data
            message = 'This is the message.  It will be repeated.'
            #print('sending "{}"'.format(message))
            self._logger.info('sending "%s"', message)
            self.sock.sendall(message)

            # Look for the response
            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                # nico: Is there a special need for a 16 Byte buffer?
                data = self.sock.recv(16)
                amount_received += len(data)
                #print('received "{}"'.format(data))
                self._logger.info('received "%s"', data)

        finally:
            print('closing socket')
            self.sock.close()
