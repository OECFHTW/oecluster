#!/usr/bin/env python3
# Author: Dennis Strasser mailto:dennis.f.strasser@gmail.com

__version__ = "1.0"

import socket
import ipaddress
import Host
import ConfigReader


class NetworkMapper(object):
    """The class maps the network to find eligible hosts for the cluster.
    This class holds a list of hosts in the current network(-segment)
     the cell phone number and the email address.
    """

    def __init__(self, ip_list = []):
        """Initializes class
        :param ip_list: list of IP-addresses. If passed, network will not be scanned.
        """
        self.config_reader = ConfigReader.ConfigReader()

        if len(ip_list) == 0:
            self._host_list = self.scan_network()
        else:
            self._host_list = self.fill_host_list(ip_list)

    def scan_network(self):
        network = self.config_reader.get_config_section("Networking")['network']
        netmask = self.config_reader.get_config_section("Networking")['netmask']
        my_net = ipaddress.ip_network(network+'/'+netmask)


        addr_range = "192.168.0.%d"
        host_list = []

        # Use UDP.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2.0)

        for ip in my_net:
            try:
                # print(ip)
                host = self.generate_host(ip)
                if host is not None:
                    host_list.append(host)
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
                host = self.generate_host(ip)
                if host is not None:
                    host_list.append(host)
            except socket.herror as ex:
                pass

        return host_list

    def generate_host(self, ip):
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

    @property
    def get_host_list(self):
        """This property returns a list of Hosts in the current network(-segment)
        :return: device_list
        """
        return self._host_list

    if __name__ == "__main__":
        print("This class should not be called directly.")