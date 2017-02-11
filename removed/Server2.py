#!/usr/bin/env python3
# Author: Dennis Strasser mailto:dennis.f.strasser@gmail.com

import socketserver
import ConfigReader
import logging

logger = logging.getLogger("networkmapper")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(name)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class ClusterRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, newClientCallback = None, dataReceivedCallback = None):
        self._newClientCallback = newClientCallback
        self._dataReceivedCallback = dataReceivedCallback
        # super().__init__()

    def setup(self):
        print(self.client_address, 'connected!')
        # self._newClientCallback(self.client_address)
        self._newClientCallback(self.client_address)
        self.request.send('hi ' + str(self.client_address) + '\n')

    def handle(self):
        while 1:
            data = self.request.recv(1024)
            self._dataReceivedCallback(self.client_address, data)
            self.request.send(data)
            if data.strip() == 'bye':
                return

    def finish(self):
        print(self.client_address, 'disconnected!')
        self.request.send('bye ' + str(self.client_address) + '\n')


# server host is a tuple ('host', port)
#server = socketserver.ThreadingTCPServer(('localhost', 5000), ClusterRequestHandler)
#server.serve_forever()


class Server2(object):
    def __init__(self, newClientCallback=None, dataReceivedCallback=None):
        self._config_reader = ConfigReader.ConfigReader()
        self._port = int(self._config_reader.get_config_section("Service")['port'])
        self._clients = dict()
        self._newClientCallback = newClientCallback
        self._dataReceivedCallback = dataReceivedCallback
        self._server = socketserver.ThreadingTCPServer(
            ('', self._port), ClusterRequestHandler(self._newClientCallback, self._dataReceivedCallback)
        )

    def add_new_client_callback(self, callback):
        self._newClientCallback = callback

    def add_received_data_callback(self, callback):
        self._dataReceivedCallback = callback

    def start(self):
        logger.debug('starting server')
        self._server.serve_forever()

    def stop(self):
        logger.debug('stopping server')
        self._server.shutdown()

