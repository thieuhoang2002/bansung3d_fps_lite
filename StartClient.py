from ursina import *
from helpers.CustomLib import *
from networks.Login import LoginForm
from networks.client import MyClient
from modules.Map import Map
# from modules.Map import load_map
from helpers.database import getIpServer


# def create_client(username):
#     global my_client
#     #my_client = MyClient(username,str(getIpServer()),6000, Vec3(0,1.4,0))
#     my_client = MyClient(username,str('192.168.174.1'),6000, Vec3(0,1.4,0))

def create_client(username):
    global my_client
    ip_server = getIpServer()  # Lấy địa chỉ IP từ hàm getIpServer
    print(f"Địa chỉ IP server: {ip_server}")
    print("type of ip_server: ", type(ip_server))

    # my_client = MyClient(username, str(ip_server), 6000, Vec3(0, 1.4, 0))
    my_client = MyClient(username, str(ip_server), 6000, Vec3(0, -.5, 0))


app = Ursina()
my_client = None
Sky()
my_map = Map()
# load_map()
LoginForm([create_client])


def input(key):
    if key == Keys.escape:
        exit(0)


def update():
    global my_client
    if my_client:
        my_client.client.process_net_events()
        my_client.easy.process_net_events()
        my_client.chatMessage.scrollcustom()


def input(key):
    global my_client
    if my_client:
        my_client.input(key)


app.run()
