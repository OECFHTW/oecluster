#!/usr/bin/env python3
# Author: Dennis Strasser mailto:dennis.f.strasser@gmail.com

import ipaddress
import socket
import logging
import ConfigReader
from network import Host

__version__ = "1.0"

logger = logging.getLogger("networkmapper")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class NetworkMapper(object):
    """The class maps the network to find eligible hosts for the cluster.
    This class holds a list of hosts in the current network(-segment)
     the cell phone number and the email address.
    """

    def __init__(self):
        """Initializes class NetworkMapper.
            If a list of member IPs is found in the config, these are used.
            Otherwise the network will be scanned.
        """
        self._config_reader = ConfigReader.ConfigReader()
        ip_list = self._config_reader.get_config_section("Cluster")['members'].replace(" ", "").split(',')

        if ip_list[0] == "":
            self._host_list = self.scan_network()
        else:
            self._host_list = self.fill_host_list(ip_list)

    def scan_network(self):
        logger.info('scanning Network')
        network = self._config_reader.get_config_section("Networking")['network']
        netmask = self._config_reader.get_config_section("Networking")['netmask']
        my_net = ipaddress.ip_network(network+'/'+netmask)
        host_list = dict()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2.0)

        for ip in my_net:
            try:
                # print(ip)
                host = self._generate_host(ip)
                if host is not None:
                    host_list[ip] = host
            except socket.herror as ex:
                pass
        return host_list

    def fill_host_list(self, ip_list):
        host_list = []

        # Use UDP.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2.0)

        for ip in ip_list:
            try:
                host = self._generate_host(ip)
                if host is not None:
                    host_list.append(host)
            except socket.herror as ex:
                pass

        return host_list

    def _generate_host(self, ip):
        host = None

        # Use UDP.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2.0)

        try:
            host_name, alias, ipaddr = socket.gethostbyaddr(str(ip))
            host = Host.Host(ip, host_name)
        except socket.herror as ex:
            pass

        return host

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

    if __name__ == "__main__":
        print("This class should not be called directly.")
