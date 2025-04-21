from ursina import *
from helpers.CustomLib import *
from helpers.ipLibrary import *
from networks.database import setIpServer
from networks.server import MyServer

my_ipv4 = get_ipv4_address()
setIpServer(my_ipv4)
server = MyServer(my_ipv4, 6000)
def update():
    global server
    while 1:
        server.handle()
        if server.update_server == True:
            server.server.process_net_events()
            server.easy.process_net_events()
        
update()