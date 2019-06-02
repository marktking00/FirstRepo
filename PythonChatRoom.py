import socket
import sys
import threading

dictOfConnections = {}

def usage():
        print ("Python Chat Room")
        print ()
        print ("PythonChatRoom.py -l -p port    - Server")
        print ("PythonChatRoom.py -t TargetIP -p port    - Client")

        print("Examples: ")
        print("PythonChatRoom.py -l -p 5555")
        print("PythonChatRoom.py -t 192.168.0.1 -p 5555")
        sys.exit(0)

def TCPServer(PortNumber):
    IPAddress = "127.0.0.1"
    Address = (IPAddress, int(PortNumber))
    TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(Address)
    print("TCP Server Waiting for a client connection...")
    numberOfClient = 0
    while True:
        TCPServerSocket.listen()
        print("TCPServer listening....\n")
        TCPClientSocket, SocketAddress = TCPServerSocket.accept()
        numberOfClient+=1
        print("This is client number",  numberOfClient,  "at SocketAddress",  SocketAddress)
        newThread= threading.Thread(target=ServerLoop, args = (TCPClientSocket, SocketAddress,  numberOfClient))   
        newThread.start()
        dictOfConnections[numberOfClient] = TCPClientSocket
        if (not dictOfConnections and (numberOfClient>0)):
            print("Closing TCPServer\n")
            sys.exit(0)
        
def ServerLoop(localSocket,  localAddress,  clientNumber):
    BUFFERSIZE = 1024
    while True:
        destClientNumber = localSocket.recv(BUFFERSIZE)
        destClientNumber = destClientNumber.decode()
        if (destClientNumber == ""):
            print("Good bye!! from client", clientNumber,  "\n" )
            dictOfConnections.pop(clientNumber)
            localSocket.close()
            if not dictOfConnections:
                print("Closing ServerLoop\n")
                sys.exit()
            break
        destClientMessage = localSocket.recv(BUFFERSIZE)
        destClientSocket = dictOfConnections[int(destClientNumber)]
        destClientSocket.send(destClientMessage)
        print("Message of", destClientMessage.decode(), "sent to client ",  destClientNumber)


def TCPClient(IPAddress, PortNumber):
    BUFFERSIZE = 1024
    Address = (IPAddress, int(PortNumber))
    TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPClientSocket.connect(Address)
    sendOrReceive = input("Do you wish to (s)end or (r)eceive a message?\n")
    while (sendOrReceive == "s" or sendOrReceive == "r"):
        if (sendOrReceive == "r"):
            print("Waiting for a message. \n")
            receivedMessage = TCPClientSocket.recv(BUFFERSIZE)
            receivedMessage = receivedMessage.decode();
            print("The message received is: \n")
            print(receivedMessage)
        elif (sendOrReceive == "s"):
            destClientNumber = input("What client do you wish to send a mesg to?\n")
            TCPClientSocket.send(destClientNumber.encode())
            destClientMessage = input("What message do you wish to send?\n")
            TCPClientSocket.send(destClientMessage.encode())
        sendOrReceive = input("Do you wish to (s)end or (r)eceive a message?\n")
    TCPClientSocket.close()
    sys.exit(0)
    
def main(argv):
        if not len(sys.argv[1:]):
            usage()
        if (len(sys.argv) == 5):
                TCPClient(sys.argv[2], sys.argv[4])
        elif (len(sys.argv) == 4):
                TCPServer(sys.argv[3])
        else:
                usage()



main(sys.argv[1:])
    
        
    
    
