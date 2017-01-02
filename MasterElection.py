

class MasterElection:

    def __init__(self):
        print("Init MasterElection")

    def getMaster(self, memberList):
        print("Elect master for list " + str(memberList))
        master="127.0.0.1"
        for clusterMember in memberList:
            #TODO implement condition
            master=clusterMember
        print("Elected Master is " + master)
        return master
