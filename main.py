import socket
import network
from utime import sleep
from machine import Pin as p
ssid = 'belkin.0d8' #Your network name
password = '9eba96b9' #Your WiFi password
led= p("LED",p.OUT)
led.value(1)
#initialize I2C 

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
address = (connect(),800)
connection = socket.socket()
connection.bind(address)
connection.listen(1)
client,addr = connection.accept()

print(f"before")
client.send("data".encode())
rec = ''
while True:
    client.send("what do you want to send?".encode())
    rec = client.recv(1024)
    print("heere")
    client.send("you said: ".encode())
print(rec)
