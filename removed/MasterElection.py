from socket import inet_aton
import struct
import ipaddress

class MasterElection:

    def __init__(self):
        print("Init MasterElection")

    def getMaster(*memberlist):
        memberListSorted = sorted(memberlist, key=lambda ip: struct.unpack("!L", inet_aton(ip))[0])
        master = memberListSorted[0]
        print("Elected Master is " + master)
        return master

if __name__ == "__main__":

    test = [
        ipaddress.ip_address('192.168.102.105'),
        ipaddress.ip_address('192.168.204.111'),
        ipaddress.ip_address('192.168.99.11')
    ]
    print(min(test))
