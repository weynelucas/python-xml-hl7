import socket

from .parser import parse


RECV_BUFFER = 4096
DEFAULT_PORT = 9100


class AlfamedClient(object):
    """
    A basic, blocking, HL7 client based upon `socket`.
    
    Connects to a network server (communication port 9100) started 
    by an ALFAMED patient monitor via TCP/IP connections.

    Refresh `socket` instance after any transmission (method `read_message`) 
    to prevent connections to being cutt off by ALFAMED monitor server
    """
    def __init__(self, host, port=DEFAULT_PORT):
        self.connected = False
        
        try:
            self.addrinfo = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)[0]
            self.connect()
        except socket.gaierror:
            raise AttributeError('Invalid address')
    
    def __repr__(self):
        return '<%s: %s:%s>' % (
            self.__class__.__name__, 
            self.addrinfo[-1][0], 
            self.addrinfo[-1][-1]
        )
    
    def connect(self):
        if not self.connected:
            self.socket= socket.socket(*self.addrinfo[:3])
            self.socket.connect(self.addrinfo[-1])
            self.connected = True
            
    def close(self):
        self.socket.close()
        self.connected = False
    
    def recv_bytes(self, limit=RECV_BUFFER):
        return self.socket.recv(limit)

    def read_message(self, parse_message=True):
        self.connect()
        data = self.recv_bytes()
        self.close()
        return parse(data) if parse_message else data