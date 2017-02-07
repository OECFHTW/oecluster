from removed import MasterElection


class ClusterList:

    def __init__(self):
        print("Init ClusterList")
        self.m_master = ""
        self.m_cluster_members = []
        self.masterElector = MasterElection.MasterElection()

    def getMaster(self):
        return self.m_master

    def setMaster(self, master):
        self.m_master = master

    def addMember(self, member):
        self.m_cluster_members.append(member)
        self.m_master = self.masterElector.getMaster(self.m_cluster_members)

    def removeMember(self, member):
        self.m_cluster_members.remove(member)
        self.m_master = self.masterElector.getMaster(self.m_cluster_members)

    def getMembers(self):
        return self.m_cluster_members

