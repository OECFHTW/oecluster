import socket
import sys



# The Server class for TCP/IP communication
class Client:

    def __init__(self, server_address='localhost', port=20000):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.server_address = server_address
        self.port = port
        self.server = (server_address, port)
        #print('connecting to {} port {}'.format(self.server_address, str(self.port)))
        print >>sys.stderr, 'connecting to %s on port %s' % self.server

    def connect(self):
        self.sock.connect(self.server)
        try:

            # Send data
            message = 'This is the message.  It will be repeated.'
            #print('sending "{}"'.format(message))
            print >>sys.stderr, 'sending "%s"' % message
            self.sock.sendall(message)

            # Look for the response
            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = self.sock.recv(16)
                amount_received += len(data)
                #print('received "{}"'.format(data))
                print >>sys.stderr, 'received "%s"' % data

        finally:
            print('closing socket')
            self.sock.close()
