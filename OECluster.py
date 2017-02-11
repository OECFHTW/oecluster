#!/usr/bin/env python3
# Author: Dennis Strasser mailto:dennis.f.strasser@gmail.com

import logging

import ConfigReader
from network import NetworkMapper
from network import AsyncServer
from network import AsyncClient
import asyncio

__version__ = "1.0"

logger = logging.getLogger("oecluster")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class OECluster:
    def __init__(self) -> object:
        logger.debug("starting cluster.")
        logger.debug("reading config.")
        self._config_reader = ConfigReader.ConfigReader()
        self._network_mapper = NetworkMapper.NetworkMapper()
        self._host_list = self._network_mapper.host_list
        self._member_list = []

    # Properties

    def _get_host_list(self):
        """This property returns a list of Hosts in the current network(-segment)
        :return: _host_list
        """
        return self._host_list

    def _set_host_list(self):
        """This property set the list of Hosts in the current network(-segment)
        :return: device_list
        """
        pass

    host_list = property(_get_host_list, _set_host_list, doc='Get/set the list of eligible hosts')

    def add_member(self, client_address):
        self._member_list.append(client_address[0])
        # self._member_list[client_address] = connection
        logger.debug("new Connection from %s port %d" % (client_address[0], client_address[1]))

    def receive_data(self, peer_name, message):
        logger.debug("received %s from %s" % (message, peer_name))

    def remove_member(self, client_address):
        try:
            del self._member_list[client_address]
        finally:
            return


if __name__ == "__main__":
    cluster = OECluster()

    logger.info('eligible hosts')

    for ip, host in cluster.host_list.items():
        logger.info(host)

    input('Enter your input:')

    loop = asyncio.get_event_loop()
    AsyncServer.cluster = cluster
    # Each client connection will create a new protocol instance
    coro = loop.create_server(AsyncServer.ClusterServerClientProtocol, '127.0.0.1', 26541)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    logger.debug('Serving on {}'.format(server.sockets[0].getsockname()))

    AsyncClient.cluster = cluster

    for ip, host in cluster.host_list.items():
        client = AsyncClient.AsyncClient(str(ip))
        asyncio.async(client.connect())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the server
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()


    # server = Server2.Server2(cluster.add_member, cluster.receive_data)
    # server.start()

    print("still alive")

    # AsyncServer.AsyncServer(cluster.add_member, cluster.receive_data)
    # loop = asyncio.get_event_loop()
    # server = loop.run_forever(server.start())

    # cluster.add_member, cluster.receive_data
    # server.start()
    # import time
    # time.sleep(1)

    # client = AsyncClient.AsyncClient("localhost", b'Hello World!')
    # while True:
    #    i = 0
