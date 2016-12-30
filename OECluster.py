import Server
import Client
import netifaces as ni
import ConfigParser


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


Config = ConfigParser.ConfigParser()
Config.read("./OECluster.cfg")
#print(Config.sections())

Interface = ConfigSectionMap("Networking")['interface']
Port = int(ConfigSectionMap("Service")['port'])

#ni.ifaddresses()#('eth0')
ip = ni.ifaddresses(Interface)[2][0]['addr']

server = Server.Server(ip, Port)
server.start()

cli1 = Client.Client(ip, Port)
cli2 = Client.Client(ip, Port)
cli3 = Client.Client(ip, Port)

cli1.connect()
cli2.connect()
cli3.connect()

print ip

raw_input('Enter your input:')
server.shutdown()


