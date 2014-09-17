# Socket example in python 3
import socket
import sys
from btle import UUID, Peripheral, BTLEException
import math
import pexpect
import binascii
from _thread import *
import time
    
host=''
port=5555

def asc2hex(string_in):
    a=""
    for x in string_in:
        a = a + ("0"+((hex(ord(x)))[2:]))[-2:]
    return(a)

def threaded_client(conn):
    conn.send(str.encode('Welcome, to smartLink\n'))
    
    while True:
        
        a='s'
        while a=='s':
            try:
                bleconn = Peripheral("f1:99:d1:ce:d9:1d random")
                while True:
                    #-----------receive data from telnet---------------------
                    data=conn.recv(2048)
                    if not data:
                        a='n'
                        break
                    print("data",data[0])
                    if data[0]!=255:
                        reply = 'Server output:' +data.decode('utf-8')
                        print("raw server ouput",data.decode('utf-8'))
                        cmd=asc2hex(data.decode('utf-8')).rstrip('0d0a')
                        print("raw cmd:",cmd)
                        bleconn.writeCharacteristic(0x0011,cmd)
                        conn.sendall(str.encode(reply))
            except socket.error as e:
                if isinstance(e.args, tuple):
                    print("errno is %d" % e[0])
                    if e[0] == errno.EPIPE:
                        # remote peer disconnected
                        print("Detected remote disconnect")
                    else:
                        # determine and handle different error
                        pass
                else:
                    print("socket error ", e)

                bleconn.disconnect()
                conn.close()
                break
            except BTLEException as e:
                #conn.sendall(str.encode("ERROR!!!!"))
                print(e)
                #conn.sendall(str.encode("Try again (y/n)?"))
    bleconn.disconnect()            
    conn.close()

if __name__ == "__main__":
    #blue tooth settings
    resp=pexpect.spawn('hciconfig hci0 up')
    resp.expect('.*')
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.bind((host,port))
    except socket.error as e:
        print(str(e))
    s.listen(5)
    print('Waiting for a connection.')
    while True:
        conn,addr=s.accept()
        print('connected to:'+addr[0]+':'+str(addr[1]))
        start_new_thread(threaded_client,(conn,))

