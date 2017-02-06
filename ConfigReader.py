#!/usr/bin/env python3
# Author: Dennis Strasser mailto:dennis.f.strasser@gmail.com

__version__ = "1.0"

import configparser as cp


class ConfigReader(object):
    """This class holds information on devices in the network

    This class holds information about people and their contact information: first- and last name,
     the cell phone number and the email address.
    """

    def __init__(self, config_file = "./OECluster.cfg"):
        """Initializes and declares class attributes from the given parameters
        :param config_file: The config file to be parsed by ConfigReader
        """
        self._config_file = config_file
        self._config_parser = cp.ConfigParser()
        self._config_parser.read(config_file)

    def get_config_section(self, section):
        dict1 = {}
        options = self._config_parser.options(section)
        for option in options:
            try:
                dict1[option] = self._config_parser.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    if __name__ == "__main__":
        print("This class should not be called directly.")