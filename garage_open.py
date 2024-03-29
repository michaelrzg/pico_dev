import network
import socket
from time import sleep

ssid = "Michael"
password = 'michaell'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def pressGarage():
    pass

try:
    ip = connect()
except KeyboardInterrupt:
    print("Exception Caught")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 54545

s.bind(ip,port)
print("connected")

while True:
    c, addr = s.accept()
    print ('Got connection from', addr )
    c.close()