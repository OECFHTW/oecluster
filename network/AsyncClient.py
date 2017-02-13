import asyncio
import ConfigReader
import logging
import sys

logger = logging.getLogger("asyncclient")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(name)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)
cluster = None

class AsyncClient(object):
    def __init__(self, target='127.0.0.1',  message='JOIN'):
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
        try:
            logger.debug("Trying to  connect to %s" % self._target)
            #yield from
            yield from asyncio.async(self._loop.create_connection(
                lambda: ClusterClientProtocol(self._message, self._loop), self._target, self._port
            ))

        except ConnectionRefusedError:
            logger.info("Connection refused by %s. Likely not running cluster service." % self._target)
        except TimeoutError:
            logger.error('Timeout error on Host: %s' % self._target)
        except Exception as e:
            #e = sys.exc_info()  # [0]
            logger.error('Caught some other error:{} Host: {}'.format(e, self._target))


class ClusterClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self._message = message
        self._loop = loop
        self._transport = None
        self._peer_name = None

    def connection_made(self, transport):
        self._transport = transport
        self._peer_name = transport.get_extra_info('peername')
        cluster.add_member(self._peer_name, self)
        transport.write(self._message.encode())
        logger.debug('Data sent to{}: {!r}'.format(self._peer_name, self._message))

    def data_received(self, data):
        logger.debug('Data received from {}: {!r}'.format(self._peer_name, data.decode()))
        cluster.receive_data(self._peer_name, data)
        # logger.debug('Closing Connection again')
        # self._transport.close()
        # self._loop.stop()

    def connection_lost(self, exc):
        logger.info('The server closed the connection')
        logger.info('Stopping the event loop')
        self._transport.close()
        self._loop.stop()

    def send(self, message):
        self._transport.write(message.encode())

