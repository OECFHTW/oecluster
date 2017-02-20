#!/usr/bin/env python3
# Author: Dennis Strasser mailto:dennis.f.strasser@gmail.com

import logging
import asyncio

__version__ = "1.0"

logger = logging.getLogger("masterelector")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(name)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)

cluster = None

class MasterElector(object):
    def __init__(self):
        self._master = None
        self._last_elected = None

    @asyncio.coroutine
    def elect_master(self):
            old_master = self._master
            if len(cluster.member_list) > 0:
                self._master = cluster.member_list[min(list(cluster.member_list.keys()))]
                if self._master != self._last_elected and hasattr(self._master.server_connection, 'peer_name'):
                    logger.info("Electing Master: {}".format(self._master.server_connection.peer_name[0]))
                    self._inform_new_master()
            yield

    # @asyncio.coroutine
    def _inform_new_master(self):
        # yield from
        self._master.send('UPVOTE')
        logger.debug("Elected new master: %s", str(self._master))
        self._last_elected = self._master



