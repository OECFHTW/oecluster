#!/usr/bin/env python3

__version__ ="0.1"

# Author: ???


class ClusterList:
    """<Short Class Description>

    <Long Class Description>
    """

    def __init__(self):
        """Shall initialize the attributes and fields

        m_master is the <IP/Hostname/Mac-Adr> of the elected master node.
        m_cluster_members is a list of <IP/Hostname/Mac-Adr> of all nodes registered to the cluster.
        """
        # a node may be an object - master=special node
        self.m_master = ""
        # think about using a dict instead of a list to save.
        self.m_cluster_members = []


# nico: take a look at python properties and think about the "uniqueness" of lists.
# Moreover, define which information you want to save within the collection
# (<IP/Hostname/Mac-Adr/Names/Last-time-active/etc.> of nodes?)


    def get_master(self):
        """Returns the <IP/Hostname/Mac-Adr> of the master node

        :return: the <IP/Hostname/Mac-Adr> of the master node
        """
        return self.m_master

    def set_master(self, master):
        """Sets the master node to the given <IP/Hostname/Mac-Adr>??

        :param master: The <IP/Hostname/Mac-Adr> of the master node
        :return: None
        """
        self.m_master = master

    def add_member(self, member):
        """Adds a member (=node) to the cluster

        :param member: The <IP/Hostname/Mac-Adr> of the member to add
        :return: None
        """
        self.m_cluster_members.append(member)

    def remove_member(self, member):
        """Removes the given node/member from the cluster

        :param member: The <IP/Hostname/Mac-Adr> of the member to remove
        :return: None
        """
        self.m_cluster_members.remove(member)

    def get_members(self):
        """Returns all nodes of the cluster

        :return: All nodes of the cluster
        """
        return self.m_cluster_members

