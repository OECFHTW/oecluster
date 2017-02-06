#!/usr/bin/env python3
# Author: Dennis Strasser mailto:dennis.f.strasser@gmail.com

__version__ = "1.0"


class Host(object):
    """This class holds information on devices in the network

    This class holds information about people and their contact information: first- and last name,
     the cell phone number and the email address.
    """

    def __init__(self, ip_address, host_name):
        """Initializes and declares class attributes from the given parameters
        :param ip_address: The IP-address of the network device
        :param host_name: The host name of the network device
        """
        self._ip_address = ip_address
        self._host_name = host_name

    def __str__(self):
        return "%s : %s" % (self._ip_address, self._host_name)


    @property
    def get_ip_address(self):
        """This is the ip_address property and returns the ip_address
        :return: ip_address
        """
        return self._ip_address

    def get_host_name(self):
        """This is the host_name property and returns the host_name
        :return: ip_address
        """
        return self._host_name

    if __name__ == "__main__":
        print("This class should not be called directly.")