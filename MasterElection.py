from socket import inet_aton
import struct

class MasterElection:

    def __init__(self):
        print("Init MasterElection")

    def getMaster(self, *memberList):
        memberListSorted = sorted(memberList, key=lambda ip: struct.unpack("!L", inet_aton(ip))[0])
        master = memberListSorted[0]
        print("Elected Master is " + master)
        return master
