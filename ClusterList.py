class ClusterList:

    def __init__(self):
        self.m_master = ""
        self.m_cluster_members = []

    def getMaster(self):
        return self.m_master

    def setMaster(self, master):
        self.m_master = master

    def addMember(self, member):
        self.m_cluster_members.append(member)

    def removeMember(self, member):
        self.m_cluster_members.remove(member)

    def getMembers(self):
        return self.m_cluster_members

