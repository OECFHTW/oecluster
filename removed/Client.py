import socket
import sys
import logging
import ConfigReader

# The Server class for TCP/IP communication

logger = logging.getLogger("networkmapper")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(name)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class Client:
    def __init__(self, server_address='localhost'):
        self._config_reader = ConfigReader.ConfigReader()
        self._port = 26541 # self._config_reader.get_config_section("Service")['port']
        # Create a TCP/IP socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self._server_address = server_address
        self._server = (server_address, self._port)
        logger.info('connecting to %s on port %s' % self._server + '\n')

    def connect(self):
        self._sock.connect(self._server)
        try:

            # Send data
            message = b'This is the message.  It will be repeated.'
            logger.info('sending "%s"' % message + '\n')
            self._sock.sendall(message)

            # Look for the response
            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = self._sock.recv(1024)
                amount_received += len(data)
                logger.info('received "%s"' % data + '\n')

        finally:
            print('closing socket')
            self._sock.close()


if __name__ == "__main__":
    client = Client()
    client.connect()
