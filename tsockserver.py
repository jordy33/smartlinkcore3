import socketserver
from threading import Thread
# https://gist.github.com/tsuna/1563257
class service(socketserver.BaseRequestHandler):
    def handle(self):
        data = 'dummy'
        print ("Client connected with: ", self.client_address)
        while len(data):
            data = self.request.recv(1024)
            self.request.send(data)

        print("Client exited")
        self.request.close()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    server=ThreadedTCPServer(('',1520), service)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
