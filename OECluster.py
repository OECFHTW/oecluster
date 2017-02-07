#!/usr/bin/env python3
# Author: Dennis Strasser mailto:dennis.f.strasser@gmail.com

import configparser as cp
import netifaces as ni
import ConfigReader
import logging
from network import NetworkMapper

__version__ = "1.0"

logger = logging.getLogger("oecluster")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class OECluster:
    def __init__(self):
        logger.debug("starting cluster.")
        logger.debug("reading config.")
        self._config_reader = ConfigReader.ConfigReader()


        self._config_reader = ConfigReader.ConfigReader()
        self._network_mapper = NetworkMapper.NetworkMapper()
        self._host_list = self._network_mapper.host_list

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
    cluster = OECluster()
    hosts_list = cluster.host_list
    logger.info('eligible hosts')

    for ip, host in hosts_list.items():
        logger.info(host)

    input('Enter your input:')



