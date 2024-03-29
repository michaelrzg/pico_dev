import machine
import utime
ledPin=machine.Pin(25, machine.Pin.OUT)
print("heresi")

while True:
    utime.sleep(.5)
    print("here1")
    ledPin.value(1)
    print("here2")
    utime.sleep(.5)
    ledPin.value(0)