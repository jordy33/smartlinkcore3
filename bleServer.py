from btle import Peripheral,BTLEException
import struct
import math
import pexpect
import binascii
import socketserver
from threading import Thread

# https://gist.github.com/tsuna/1563257

def asc2hex(string_in):
    a=""
    for x in string_in:
        a = a + ("0"+((hex(ord(x)))[2:]))[-2:]
    return(a)

class service(socketserver.BaseRequestHandler):
    def handle(self):
        data = 'dummy'
        print ("Client connected with: ", self.client_address)
        devaddr = "f1:99:d1:ce:d9:1d random"
        bleconn = Peripheral(devaddr)
        while len(data):
            data = self.request.recv(1024)
            self.request.send(data)
            cmd=asc2hex(data.decode('utf-8')).rstrip('0d0a')
            print ("data",len(data))
            if len(data)!=0:
                bleconn.writeCharacteristic(0x0011,cmd)

        print("Client exited")
        bleconn.disconnect()
        self.request.close()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    # activate bluetooth
    resp=pexpect.spawn('hciconfig hci0 up')
    resp.expect('.*')
    print ("Smartlink Server started")
    server=ThreadedTCPServer(('',1520), service)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
