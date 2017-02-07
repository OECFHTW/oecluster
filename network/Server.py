import socket
import sys
import threading


# The Server class for TCP/IP communication
class Server:
    def __init__(self, address='localhost', port=20000):
        self.address = address
        self.port = port
        self.Clients = dict()

        # Create a TCP/IP socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        self.server_address = (self.address, self.port)

    def start(self):
        sys.stderr.write('starting up on %s port %s' % self.server_address + '\n')
        self._socket.bind(self.server_address)

        # Listen for incoming connections
        self._socket.listen(5)
        thread = threading.Thread(target=self.accept, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
        #self.accept()

    def accept(self):
        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = self._socket.accept()
            self.Clients[client_address] = connection
            sys.stderr.write('new connection registered! Client address : ' + str(client_address) + '\n')

            try:
                print('connection from', client_address)

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16)
                    sys.stderr.write('received "%s"' % data + '\n')
                    if data:
                        sys.stderr.write('sending data back to the client\n')
                        connection.sendall(data)
                    else:
                        sys.stderr.write('no more data from'+ str(client_address) + '\n')
                        break

            finally:
                    #print >>sys.stderr, 'finally'
                    sys.stderr.write('finally\n')
                    # Clean up the connection
                    # connection.close()

    def shutdown(self):
        #for client in self.Clients:
            #client.close()
        #self.sock.shutdown(socket.SHUT_RDWR)
        self._socket.close()
