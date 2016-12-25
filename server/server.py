#!/usr/bin/env python3
from util.config.logger import Log

__version__ = "0.1"

# Author: Funny program style guy & friends

import socket
import sys
import threading

# nico: Take a look at TCPServer and read into stopping a threads.



# The Server class for TCP/IP communication
class Server:

    def __init__(self, address='localhost', port=20000):
        """I, the funny program style guy or my friends, will document this class.

        :param address:
        :param port:
        """

        self._logger = Log.get_logger(self.__class__.__name__)
        self._address = address
        self._port = port
        self._clients = {}
        # Create a TCP/IP socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        self.server_address = (self._address, self._port)

    def start(self):
        """This needs documentation as well.

        :return: None
        """
        self._logger.info('starting up on %s port %s', self._address, self._port)
        self._sock.bind(self.server_address)
        # Listen for incoming connections
        self._sock.listen(5)
        thread = threading.Thread(target=self.accept, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def accept(self):
        """Ouch, this method unifies so much that documentation may even hurt.

        :return: None
        """
        while True:
            # Wait for a connection
            self._logger.info('waiting for a connection')
            connection, client_address = self._sock.accept()
            self._clients[client_address] = connection
            self._logger.info('new connection registered! Client address : %s', client_address)

            try:
                # nico: redundancy is safety?
                self._logger.info('connection from', client_address)

                # nico: Why do you need "small chunks"?

                # Receive the data in small chunks and retransmit it
                while True:
                    # nico: I do not get why your buffer only takes 16 bytes.
                    data = connection.recv(16)
                    self._logger.info('received "%s"', data)
                    if data:
                        self._logger.info('sending data back to the client')
                        connection.sendall(data)
                    else:
                        self._logger.info('no more data from %s', client_address)
                        break

            finally:
                # nico: when is finally called and what do you want to do after it was reached?
                self._logger.info('finally')
                # Clean up the connection
                # connection.close()
