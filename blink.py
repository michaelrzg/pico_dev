import machine
import utime
import bme280
ledPin=machine.Pin("LED", machine.Pin.OUT)
sensor = machine.ADC(4)
while True:
    print(27 - ((sensor.read_u16()*(3.3/(65535))-0.706)/0.001721))
    utime.sleep(.5)
    ledPin.value(1)
    utime.sleep(.5)
    ledPin.value(0)