import asyncio
import ConfigReader
import logging

logger = logging.getLogger("asyncclient")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(name)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)
cluster = None

class AsyncClient(object):
    def __init__(self, target='127.0.0.1',  message='Hello Server!'):
        self._loop = asyncio.get_event_loop()
        self._config_reader = ConfigReader.ConfigReader()
        self._port = self._config_reader.get_config_section("Service")['port']
        self._target = target
        self._message = message
        self._co_routine = None

        # self._loop.run_until_complete(self._co_routine)
        # self._loop.run_forever()
        # self._loop.close()

    @asyncio.coroutine
    def connect(self):
        self._co_routine = self._loop.create_connection(
            lambda: EchoClientProtocol(self._message, self._loop), self._target, self._port
        )
        asyncio.async(self._co_routine)


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self._message = message
        self._loop = loop
        self._transport = None
        self._peername = None

    def connection_made(self, transport):
        self._transport = transport
        self._peername = transport.get_extra_info('peername')
        transport.write(self._message.encode())
        logger.debug('Data sent: {!r}'.format(self._message))

    def data_received(self, data):
        logger.debug('Data received: {!r}'.format(data.decode()))
        cluster.receive_data(self._peername, data)
        logger.debug('Closing Connection again')
        # self._transport.close()
        # self._loop.stop()

    def connection_lost(self, exc):
        logger.info('The server closed the connection')
        logger.info('Stopping the event loop')
        self._transport.close()
        self._loop.stop()

