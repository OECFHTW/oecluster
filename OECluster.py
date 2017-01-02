import Server
import Client
import ClusterList
import netifaces as ni
import configparser as cp

#python 3 needed

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

print("Starting application")

print("Available Interfaces: "+str(ni.interfaces()))
print("Reading config")
Config = cp.ConfigParser()
Config.read("./OECluster.cfg")
#print(Config.sections())

Interface = ConfigSectionMap("Networking")['interface']
Port = int(ConfigSectionMap("Service")['port'])

print("Init with Interface "+ Interface + " & Port "+ str(Port))
#ni.ifaddresses()#('eth0')
myip = ni.ifaddresses(Interface)[2][0]['addr']
print("IP "+ myip)

clusterlist = ClusterList.ClusterList()
clusterlist.addMember(myip)

server = Server.Server(myip, Port)
server.start()

cli1 = Client.Client(myip, Port)
cli2 = Client.Client(myip, Port)
cli3 = Client.Client(myip, Port)

cli1.connect()
cli2.connect()
cli3.connect()

print(myip)

input('Enter your input:')
server.shutdown()


