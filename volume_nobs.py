import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import machine
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# i2cAddr = x        #here put the address from print(I2C.scan)
# [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]
# [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]

# [][][][][]
# [][][][][]
# [][][][][]
# [][][][][]
# [][][][][]
# [][][][][]
# [][][][][]
# [][][][][]

i2cRows = 16
i2cColumns = 2

i2c = I2C(0, sda=machine.Pin(x), scl=machine.Pin(y), freq=400000)  # TODO update x and y to pins you connect the i2c
lcd = I2cLcd(i2c, i2cAddr, i2cRows, i2cColumns)

i2c2 = I2C(0, sda=machine.Pin(x), scl=machine.Pin(y), freq=400000)  # TODO update x and y to pins you connect the i2c
lcd2 = I2cLcd(i2c2, i2cAddr, i2cRows, i2cColumns)

discordSymbol = [
    0x00,
    0x1F,
    0x0E,
    0x15,
    0x1F,
    0x1B,
    0x00,
    0x00
]

index = 1
ani = [
    # portal 
    [ 0x1F,
      0x11,
      0x11,
      0x11,
      0x11,
      0x11,
      0x11,
      0x1F
    ],
    # charicature 
    [ 0x0E,
      0x0A,
      0x0E,
      0x14,
      0x1F,
      0x05,
      0x0E,
      0x11
    ]
    ]

def updateScreen(masterBars, discordBars, miscBars):

    global index

    # first lcd screen init
    lcd.clear()
    lcd.move_to(0, 0)

    # update screen 1 with data

    mtrvolbar = ""
    for i in range(0, masterBars):
        mtrvolbar += "-"
    lcd.move_to(0,0)
    lcd.putstr("main>" + mtrvolbar + "<")
    lcd.move_to(0,1)
    lcd.custom_char(0, discordSymbol)
    lcd.move_to(1,1)
    disbar=""
    for i in range(0,discordBars):
        disbar += "-"
    lcd.putstr("dis>"+disbar+"<")
    
    misc=""
    for i in range(0,miscBars):
        misc += "-"

    # second lcd screen init

    lcd2.clear()
    lcd2.move_to(0, 0)

    # second screen update

    lcd2.putstr("misc>"+misc)
    lcd2.move_to(0,1)

    # luh animation yfm

    lcd2.custom_char(0, ani[0])
    lcd2.custom_char(index, ani[1])
    lcd2.custom_char(15, ani[0])
    index += 1
    if index > 14:
        index = 1



def map(x, in_min, in_max, out_min, out_max):
    return ((x - in_min) * (out_max - out_min)) / (in_max - in_min) + out_max


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# pot1=ADC(Pin(28))
pot1Value = 0  # this nob will be master volume
prevPot1 = 0
# pot2=ADC(27)
pot2Value = 0  # this nob will be Discord Volume
prevPot2 = 0

# pot3 = ADC(28)     #this nob will control all other programs
pot3Value = 0
prevPot3 = 0

while True:
    time.sleep(.4)
    all_devices = AudioUtilities.GetAllSessions()
    # pot1Value=pot1.read_u16()/65535
    if pot1Value - prevPot1 > 20 or pot1Value - prevPot1 < -20:
        prevPot1 = pot1Value
        volume.SetMasterVolumeLevelScalar((pot1Value) * 100)
    # pot2Value=pot1.read_u16()
    if pot2Value - prevPot2 > 20 or pot2Value - prevPot2 < -20:
        prevPot2 = pot2Value
        for session in all_devices:
            if session.Process and session.Process.name() == "Discord.exe":
                thisVol = session._ctl.QueryInterface(ISimpleAudioVolume)
                thisVol.SetMasterVolume(pot2Value, None)
    # pot3Value=pot1.read_u16()
    if pot3Value - prevPot3 > 20 or pot3Value - prevPot3 < -20:
        prevPot3 = pot3Value
        for session in all_devices:
            if session.Process and session.Process.name() != "Discord.exe":
                thisVol = session._ctl.QueryInterface(ISimpleAudioVolume)
                thisVol.SetMasterVolume(pot3Value, None)
