import machine
import utime

pot1 = ADC(Pin(28))

while True:
    print(pot.read_u16())
    utime.sleep(.1)