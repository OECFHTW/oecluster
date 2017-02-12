#!/usr/bin/env python3
# Author: Dennis Strasser mailto:dennis.f.strasser@gmail.com

import logging

__version__ = "1.0"

logger = logging.getLogger("masterelector")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(name)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class MasterElector(object):
    def __init__(self):
        self._master = None

    def elect_master(self, node_dictionary):
        self._master = min(list(node_dictionary.keys()))
        logger.debug("Elected new master: %s", str(self._master))
        # TODO add if master changed
        return self._master



