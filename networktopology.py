#!/usr/bin/env python3

#Author: Susanne&Stephan&Roman

__version__ = "0.1"

# nico:
# I like the idea of pinging all available hosts within a network range.
# Brute force style :D

# template for pinging IP range
import subprocess

from util.config.logger import Log


class Network:
    @staticmethod
    def ping(self, adr_range):
        for ping in range(1,255):
            address = (adr_range + str(ping))
            res = subprocess.call(['ping', '-c', '3', address])

            result_str = 'OK' if res==0 else 'NO RESPONSE'
            Log.info(self, "ping to %s address %d:%s", address, res, result_str)

#   find all differences in the 2 lists

listOrigin = ["192.168.123#192.168.13"]
listActual = ["192.168.123#192.168.13#192.168.1.13"]

# a set is not a list :P
result = set(listOrigin).symmetric_difference(listOrigin)

#