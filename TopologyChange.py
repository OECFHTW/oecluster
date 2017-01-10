#Author Susanne&Stephan&Roman
#new comment added

'''
# template for pinging IP range
import subprocess

for ping in range(1,255):
    address = "192.168.1." + str(ping)
    res = subprocess.call(['ping', '-c', '3', address])
    if res == 0:
        print "ping to", address, "OK"
    elif res == 2:
        print "no response from", address
    else:
        print "ping to", address, "failed!"

#   find all differences in the 2 lists

listOrigin = ["192.168.123#192.168.13"]
listActual = ["192.168.123#192.168.13#192.168.1.13"]

result = set(listOrigin).symmetric_difference(listOrigin)

#
'''

import MasterElection
import ClusterList
import Client
import Server

class TopologyChange:

    def __init__(self, clusterlist, server, client):

    def compareList(newMemberlist, oldMemberlist):
        #TODO: Compare two Lists
        #actualList = Clusterlist.

        listOrigin = ["192.168.123#192.168.13"]
        listActual = ["192.168.123#192.168.13#192.168.1.13"]

        result = set(listOrigin).symmetric_difference(listOrigin)

        MasterElection.getMaster(result)

        return()







