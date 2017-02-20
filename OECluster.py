#!/usr/bin/env python3
# Author: Dennis Strasser mailto:dennis.f.strasser@gmail.com

import asyncio
import ipaddress
import logging
import socket
import time
import ConfigReader
from cluster import MasterElector
from network import NetworkMapper
from network import AsyncServer
from network import AsyncClient

__version__ = "1.0"

logger = logging.getLogger("oecluster")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class OECluster(object):
    def __init__(self):
        logger.debug("starting cluster.")
        logger.debug("reading config.")
        self._config_reader = ConfigReader.ConfigReader()
        self._network_mapper = NetworkMapper.NetworkMapper()
        MasterElector.cluster = self
        self._master_elector = MasterElector.MasterElector()
        self._host_list = self._network_mapper.host_list
        self._member_list = {}
        self._continuous_scan = bool(self._config_reader.get_config_section("Cluster")['continuously_scan'])
        self._scan_interval = int(self._config_reader.get_config_section("Cluster")['scan_interval'])
        self._port = int(self._config_reader.get_config_section("Service")['port'])
        self.loop = asyncio.get_event_loop()
        self._master_counter = 0
        self._is_master = False

    def add_member(self, client_address, connection, is_client=False):
        node_ip = ipaddress.ip_address(client_address[0])

        if is_client:
            self._host_list[node_ip].client_connection = connection
            logger.debug("new Connection from %s port %d" % (client_address[0], client_address[1]))
            logger.debug("Connecting to %s" % str(node_ip))

        else:
            self._host_list[node_ip].server_connection = connection
            logger.debug("Connected to %s" % str(node_ip))

        self._member_list[node_ip] = self._host_list[node_ip]
        # self._master_elector.elect_master(self._member_list)
        # TODO add if master changed

    def receive_data(self, peer_name, message, is_client=False):
        message = message.decode()
        logger.debug("received %s from %s" % (message, peer_name))
        if is_client:
            if message == 'JOINUPVOTE':
                self._increase_master_counter()
        else:
            if message == 'ACKNOWLEDGE':
                logger.info("%s accepted master election" % peer_name)

    def _increase_master_counter(self):
        self._master_counter += 1
        if self._master_counter == len(self._member_list):
            self._is_master = True
            logger.info("This Node has been elected as master")
            for key, member in self._member_list.items():
                member.send("ACKNOWLEDGE")

    def remove_member(self, client_address):
        try:
            del self._member_list[client_address]
        finally:
            return

    @asyncio.coroutine
    def contiuously_scan_network(self):
        while True:
            # yield from asyncio.sleep(self._scan_interval)
            # asyncio.sleep(self._scan_interval)
            new_host_list = self._network_mapper.scan_network()

            for key in new_host_list.keys():
                if key not in self._host_list:
                    self._host_list[key] = new_host_list[key]
                # logger.info(self._host_list[key])
            yield  # from self

    @asyncio.coroutine
    def connect_to_nodes(self):
        while True:
            for ip, host in self._host_list.items():
                if ip == ipaddress.ip_address('192.168.0.246'):
                    xyz = 0

                if ip not in self._member_list or self._member_list[ip].server_connection is None:
                    #if not hasattr(self._host_list[ip].server_connection, 'test'):
                    if not (
                            type(self._host_list[ip].server_connection) is AsyncClient
                            or hasattr(self._host_list[ip].server_connection, 'peer_name')
                    ):
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(0.05)
                        port = self._port
                        if sock.connect_ex((str(ip), port)) == 0:
                            self._host_list[ip].server_connection = client = AsyncClient.AsyncClient(str(ip))
                            yield from asyncio.async(client.connect())
                        else:
                            logger.debug('Cluster not running on {}'.format(self._host_list[ip]))
            yield

    @asyncio.coroutine
    def elect_master(self):
        # pass
        while True:
            yield from self._master_elector.elect_master()

    def get_own_ip(self):
        return ([l for l in (
            [ip_addr for ip_addr in socket.gethostbyname_ex(socket.gethostname())[2] if not ip_addr.startswith("127.")][:1],
            [
                [
                    (s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
                    [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
                    ][0][1]]
        ) if l][0][0])
        # TODO bereinigen, das muss besser gehen

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
    
    def _get_member_list(self):
        """This property returns a list of members in the cluster
        :return: _member_list
        """
        return self._member_list

    def _set_member_list(self):
        """This property set the list of members in the cluster
        :return: device_list
        """
        pass

    member_list = property(_get_member_list, _set_member_list, doc='Get/set the list of cluster members')


if __name__ == "__main__":
    cluster = OECluster()

    # TODO checken, ob das nicht besser in eine MAIN-Methode des Cluster soll?!

    #logger.info('eligible hosts')

    #for ip, host in cluster.host_list.items():
    #    logger.info(host)

    #input('Enter your input:')

    loop = cluster.loop
    AsyncServer.cluster = cluster
    # Each client connection will create a new protocol instance
    coro = loop.create_server(AsyncServer.ClusterServerClientProtocol, '', 26541)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    logger.debug('Serving on {}'.format(server.sockets[0].getsockname()))

    AsyncClient.cluster = cluster
    asyncio.async(cluster.contiuously_scan_network())
    asyncio.async(cluster.connect_to_nodes())
    asyncio.async(cluster.elect_master())


    # for ip, host in cluster.host_list.items():
    #    client = AsyncClient.AsyncClient(str(ip))
    #    asyncio.async(client.connect())

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
