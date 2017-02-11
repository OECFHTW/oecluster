import socket
import sys
import threading
import logging
import ConfigReader

logger = logging.getLogger("networkmapper")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(name)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class Server:
    # The Server class for TCP/IP communication
    def __init__(self, address='localhost', port=20000):
        self._config_reader = ConfigReader.ConfigReader()
        self._address = ""
        self._port = self._config_reader.get_config_section("Service")['port']
        self._clients = dict()
        self._newClientCallback = None
        self._lostClientCallback = None

        # Create a TCP/IP socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        self.server_address = (self._address, self._port)

    def add_new_client_callback(self, callback):
        self._newClientCallback = callback

    def add_lost_client_callback(self, callback):
        self._lostClientCallback = callback

    def start(self):
        logger.info('starting up server on %s port %d' % (self._address, self._port))
        self._socket.bind(self.server_address)

        # Listen for incoming connections
        self._socket.listen(5)
        thread = threading.Thread(target=self._accept, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
        #self._accept()

    def _accept(self):
        while True:
            # Wait for a connection
            logger.info('waiting for a connection')
            connection, client_address = self._socket.accept()
            self._clients[client_address] = connection
            self._newClientCallback(client_address, connection)
            logger.info('new connection registered! Client address : ' + str(client_address) + '\n')

            try:
                print('connection from', client_address)

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(1024)
                    logger.info('received "%s from %s"' % (data, client_address))
                    if data:
                        logger.info('sending data back to the client\n')
                        connection.sendall(data)
                    else:
                        logger.info('no more data from'+str(client_address) + '\n')
                        connection.close()
                        self._lostClientCallback(client_address)
                        # break

            finally:
                    #print >>sys.stderr, 'finally'
                    logger.info('shuttting down server\n')
                    # Clean up the connection
                    # connection.close()

    def shutdown(self):
        #for client in self.Clients:
            #client.close()
        #self.sock.shutdown(socket.SHUT_RDWR)
        self._socket.close()
