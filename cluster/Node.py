#!/usr/bin/env python3
# Author: Dennis Strasser mailto:dennis.f.strasser@gmail.com

import logging

__version__ = "1.0"

logger = logging.getLogger("node")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(name)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class Node(object):
    """This class holds information on devices in the network

    This class holds information about people and their contact information: first- and last name,
     the cell phone number and the email address.
    """

    def __init__(self, ip_address, host_name=""):
        """Initializes and declares class attributes from the given parameters
        :param ip_address: The IP-address of the network device
        :param host_name: The host name of the network device
        """
        self._ip_address = ip_address
        self._host_name = host_name
        self._is_cluster_member = False
        self._client_connection = None
        self._server_connection = None

    def send(self, message):
        logger.debug("sending message to {} : {}".format(self._server_connection._peer_name[0], message))
        self._server_connection.send(message)

    def __str__(self):
        return "%s : %s | cluster member: %s" % (self._ip_address, self._host_name, self._is_cluster_member)


    # Properties
    def _get_ip_address(self):
        """This property returns the IP address
        :return: _ip_address
        """
        return self._ip_address

    def _set_ip_address(self, val):
        """This property sets the IP address
        """
        pass

    ip_address = property(_get_ip_address,
                                 _set_ip_address,
                                 doc='Get/set the connection where host is client'
                                 )
    
    def _get_host_name(self):
        """This property returns connection where host is client
        :return: _host_name
        """
        return self._host_name

    def _set_host_name(self, val):
        """This property sets the connection where host is client
        """
        self._host_name = val

    host_name = property(_get_host_name,
                                 _set_host_name,
                                 doc='Get/set the connection where host is client'
                                 )
    
    def _get_client_connection(self):
        """This property returns connection where host is client
        :return: _client_connection
        """
        return self._client_connection

    def _set_client_connection(self, val):
        """This property sets the connection where host is client
        """
        self._client_connection = val
        self._is_cluster_member = True

    client_connection = property(_get_client_connection,
                                 _set_client_connection,
                                 doc='Get/set the connection where host is client'
                                 )
    
    def _get_server_connection(self):
        """This property returns connection where host is server
        :return: _server_connection
        """
        return self._server_connection

    def _set_server_connection(self, val):
        """This property sets the connection where host is server
        """
        self._server_connection = val
        self._is_cluster_member = True

    server_connection = property(_get_server_connection,
                                 _set_server_connection,
                                 doc='Get/set the connection where host is server'
                                 )
    
    def _get_is_cluster_member(self):
        """This property returns connection where host is server
        :return: _is_cluster_member
        """
        return self._is_cluster_member

    def _set_is_cluster_member(self, val):
        """This property sets the connection where host is server
        """
        pass

    is_cluster_member = property(_get_is_cluster_member,
                                 _set_is_cluster_member,
                                 doc='Get/set the connection where host is server'
                                 )

    if __name__ == "__main__":
        print("This class should not be called directly.")
