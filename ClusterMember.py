#!/usr/bin/env python3
# Author: Dennis Strasser mailto:dennis.f.strasser@gmail.com

__version__ = "1.0"

import Host


class ClusterMember(Host):
    """This class holds information on devices in the network

    This class holds information about people and their contact information: first- and last name,
     the cell phone number and the email address.
    """

    def __init__(self, ip_address, host_name):
        """Initializes and declares class attributes from the given parameters
        :param ip_address: The IP-address of the network device
        :param host_name: The host name of the network device
        """
        Host._init__(self, ip_address, host_name)
