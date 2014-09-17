from btle import UUID, Peripheral, BTLEException
import struct
import math
import pexpect
import binascii

#class KeypressSensor(SensorBase):
# TODO: only sends notifications, you can't poll it
#    svcUUID = UUID(0xFFE0)
# write 0100 to 0x60
# get notifications on 5F

class SensorTag(Peripheral):
    def __init__(self,addr):
        Peripheral.__init__(self,addr)
        self.discoverServices()

def asc2hex(string_in):
    a=""
    for x in string_in:
        a = a + ("0"+((hex(ord(x)))[2:]))[-2:]
    return(a)

if __name__ == "__main__":
    import time

    #tag = SensorTag("BC:6A:29:AB:D3:7A")
    
    resp=pexpect.spawn('hciconfig hci0 up')
    resp.expect('.*')
    Debugging = False
    #devaddr = sys.argv[1] + " random"
    devaddr = "f1:99:d1:ce:d9:1d random"
    print("Connecting to:", devaddr)
    a='s'
    while a=='s':
        try:
            conn = Peripheral(devaddr)
            while True:
                n = input("Ponga (s) para salir:")
                cmd=asc2hex(n)
                try:
                    conn.writeCharacteristic(0x0011,cmd)
                except BTLEException as e:
                    print ("write error:")
                    print (e)
                    print ("Try again? (s/n)")
                    b=input()
                    if b == 's':
                        a='s'
                        break
                else:
                    b='n'
                if n.strip() == 's':
                    a='n'
                    break
        except BTLEException as e:
            print ("ERROR!!!!")
            print (e)
            print ("desea intentarlo de nuevo (s/n)?")
            a=input()
        finally:
            print ("saliendo")
            #conn.disconnect()
