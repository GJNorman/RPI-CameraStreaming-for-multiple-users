import zmq

"""
**********************************************************************
    Create a ZMQ socket 
    example usage
    
    mySocket = ZMQSocket("tcp://*5555",zmq.PUB,"string","Server")
    
    ProtocolIPAndPort -> http://api.zeromq.org/4-2:zmq-connect
        protocols:  tcp     -> between different processess or devices      tcp://localhost:5555
                    ipc     -> between different processes                  ipc:///tmp/test.ipc     note the 3 ///
                    inproc  -> between different threads within a process.  inproc://my-endpoint
                    
    connectionTypes: https://zguide.zeromq.org/docs/chapter2/ 
                    Publisher/Subscribe Pattern, zmq.PUB, zmq.SUB
                        Publisher sends data without checking if anyone receives
                        Subscriber reads from socket in non blocking fashion
                        supports multiple publishers and subscribers
                        Publisher is write only
                        subscriber is read only
                        
                    reply / request pattern zmq.REQ, zmq.REP
                        one REQ and multiple REPs
                        bilateral communication
                        reads must be acknowledged by writes
                        
    transmission types:
                    byte stream     "bytes"   socket.send(mystring.encode()).   socket.send(b'Hello!')
                    string          "string". socket.send(mystring)             socket.send("Hello")
                    python object   "pyobj"   socket.send(cvFrame)              
                    bytes is the most versatily
                    
                    you can convert a byte stream to a string:
                        message = socket.recv();
                        
                        message = str(message)
                        
     clientServer:
                    Server; uses "Bind"
                    Client; uses "connect"
                    
                    server should be the socket created in the most stable program
                    
     options
                    see zmq documentation
                        
**********************************************************************
"""
class ZMQSocket():

    def __init__(self,ProtocolIPAndPort:str,ConnectType = zmq.PUB, dataTransmissionType = 'bytes',clientServer = "Server",options:list=[]   ):
        self.ctx = zmq.Context.instance()
        self.Socket = self.ctx.socket(ConnectType)
        
        self.send = self.Socket.send
        self.recv = self.Socket.recv
        if len(options) != 0:
            #for x in options:
            print('options = ' +str( options) )
            self.Socket.setsockopt(options[0],options[1])
        if (dataTransmissionType.find("string") != -1):
            self.send = self.Socket.send_string
            self.recv = self.Socket.recv_string
        
        if (dataTransmissionType.find("pyobj") != -1):
            self.send = self.Socket.send_pyobj
            self.recv = self.Socket.recv_pyobj
        
        if clientServer.find("Server") != -1:
            self.Socket.bind(ProtocolIPAndPort)
        else:
            if ProtocolIPAndPort.find("://*") != -1:
                #the server is broadcasting to all available IPs; the client should connect to localhost
                point1 = ProtocolIPAndPort.find("://*") 
                point2 = ProtocolIPAndPort.find("*") + 1
                protocol = ProtocolIPAndPort[:point1]
                address = ProtocolIPAndPort[point2:]
                ProtocolIPAndPort = protocol + "://localhost" + address
            print(ProtocolIPAndPort)
            self.Socket.connect(ProtocolIPAndPort)

    def __del__(self):
        #del self.Socket
        return #self.ctx.term()
