#!/usr/bin/env python3
import asyncio
import logging
import ConfigReader
from asyncio import async

logger = logging.getLogger("asyncserver")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(name)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)
cluster = None

class AsyncServer(object):
    def __init__(self, newClientCallback=None, dataReceivedCallback=None):
        self._config_reader = ConfigReader.ConfigReader()
        self._address = "localhost"
        self._port = self._config_reader.get_config_section("Service")['port']
        self._clients = dict()
        self._newClientCallback = newClientCallback
        self._dataReceivedCallback = dataReceivedCallback
        self._loop = asyncio.get_event_loop()
        self._server = None

    def add_new_client_callback(self, callback):
        self._newClientCallback = callback

    def add_received_data_callback(self, callback):
        self._dataReceivedCallback = callback

    # @asyncio.coroutine
    def start(self):
        # Each client connection will create a new protocol instance
        # Create the server and let the loop finish the coroutine before
        # starting the real event loop.
        co_routine = self._loop.create_server(
            ClusterServerClientProtocol(self._newClientCallback, self._dataReceivedCallback), "", self._port
        )
        self._server = self._loop.run_until_complete(co_routine)
        logger.debug('starting up on {} port {}'.format("all addresses", self._port))

        # Enter the event loop permanently to handle all connections.
        try:
            asyncio.set_event_loop(self._loop)
            self._loop.run_forever()
        finally:
            logger.debug('closing server')
            self._server.close()
            self._loop.run_until_complete(self._server.wait_closed())
            self._loop.debug('closing event loop')
            self._loop.close()

    def stop(self):
        logger.debug('closing server')
        self._server.close()
        self._loop.run_until_complete(self._server.wait_closed())
        self._loop.debug('closing event loop')
        self._loop.close()


class ClusterServerClientProtocol(asyncio.Protocol):
    def __init__(self):
        self._peer_name = None
        self._transport = None

    def connection_made(self, transport):
        self._peer_name = transport.get_extra_info('peername')
        self._transport = transport
        cluster.add_member(self._peer_name, self, True)
        logger.debug('Connection from {}'.format(self._peer_name))

    def data_received(self, data):
        message = data.decode()
        logger.debug('Data received from {}: {!r}'.format(self._peer_name, message))
        cluster.receive_data(self._peer_name, data, True)
        logger.debug('Send to {}: {!r}'.format(self._peer_name, message))
        self._transport.write(data)
        # logger.debug('Close the client socket')

    def connection_lost(self, error):
        if error:
            logger.error('ERROR: {}'.format(error))
        else:
            logger.debug('closing')
        super().connection_lost(error)

    def send(self, message):
        self._transport.write(message.encode())

    # Properties
    def _get_peer_name(self):
        """This property returns the peer name
        :return: _peer_name
        """
        return self._peer_name

    def _set_peer_name(self):
        """This property sets the peer name
        """
        pass

    peer_name = property(_get_peer_name, _set_peer_name, doc='Get/set the peer name')

