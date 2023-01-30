import zmq                      #sockets
from ZMQSocketClass import ZMQSocket

class SubscriberSocketClass():
    """
    argument            type        example                         comments
    self                implicit    not required
    socket              str;        "tcp://localhost:5558"          protocol and port id Mandatory!
    recv_type           string;     "bytes"; "pyobj"; "string"      
    subscriberOptions   list;       b'',b'Error',b'Aliquoter'       message topic filters

    example

        newSocket = SubscriberSocketClass(socket="inproc://my_publisher",recv_type="pyobj")

    """
    def __init__(self, socketInfo:str, recv_type:str = "bytes", subscribeOptions:list = [b''], bufferSize=1 ):
        self.subscriber = ZMQSocket(socketInfo,zmq.SUB,recv_type, "Client",[zmq.CONFLATE,bufferSize]) 
        #keep only the most recent message
        for x in subscribeOptions:
            self.subscriber.Socket.setsockopt(zmq.SUBSCRIBE, x)

    """
    returns message from subscriber socket, along with bool indicating if successful
    example call

       msg,ret = newSocket.get_message()
       if ret == True:
           /*process message*/
       
    """
    def get_message(self):
        
        message = self.subscriber.recv()

        if message is not None:
            return message, True
                      
        return b'Read Error', False

