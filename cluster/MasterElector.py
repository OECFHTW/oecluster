#!/usr/bin/env python3
# Author: Dennis Strasser mailto:dennis.f.strasser@gmail.com

import logging
import asyncio

__version__ = "1.0"

logger = logging.getLogger("masterelector")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(name)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class MasterElector(object):
    def __init__(self):
        self._master = None

    def elect_master(self, node_dictionary):
        old_master = self._master
        self._master = min(list(node_dictionary.keys()))

        if self._master != old_master:
            # yield from
            # asyncio.async(self._inform_new_master(node_dictionary))
            self._inform_new_master(node_dictionary)

        return self._master

    # @asyncio.coroutine
    def _inform_new_master(self, node_dictionary):
        # yield from
        node_dictionary[self._master].send('UPVOTE')
        logger.debug("Elected new master: %s", str(self._master))



