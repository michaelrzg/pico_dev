#import modules
import network
import socket
from time import sleep
from machine import Pin, I2C

ssid = 'belkin.0d8' #Your network name
password = '9eba96b9' #Your WiFi password

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

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(reading):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Pico W Weather Station</title>
            <meta http-equiv="refresh" content="10">
            <style></style>
            </head>
            <body>
            <p>{reading}</p>
            </body>
            </html>
            """
    return str(html)
    
def serve(connection):
    #Start a web server
    
    while True:
        temp = "5"
        pressure = "4"
        humidity = "3"
        reading = 'Temperature: ' + temp + '. Humidity: ' + humidity + '. Pressure: ' + pressure
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)       
        html = webpage(reading)
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
    
