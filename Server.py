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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        self.server_address = (self.address, self.port)

    def start(self):
        #print('starting up on {} port {}'.format(self.address, str(self.port)))
        print >>sys.stderr, 'starting up on %s port %s' % self.server_address
        self.sock.bind(self.server_address)
        # Listen for incoming connections
        self.sock.listen(5)
        thread = threading.Thread(target=self.accept, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
        #self.accept()

    def accept(self):
        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = self.sock.accept()
            self.Clients[client_address] = connection
            print('new connection registered! Client address : {}', format(client_address))
            #print >>sys.stderr, 'new connection registered! Client address : %s' % client_address

            try:
                print('connection from', client_address)

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16)
                    print >>sys.stderr, 'received "%s"' % data
                    if data:
                        print >>sys.stderr, 'sending data back to the client'
                        connection.sendall(data)
                    else:
                        print >>sys.stderr, 'no more data from', client_address
                        break

            finally:
                    print >>sys.stderr, 'finally'
                    # Clean up the connection
                    # connection.close()
