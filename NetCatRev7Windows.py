import sys
import socket
import subprocess

def usage():
        print ("Netcat Replacement")
        print ()
        print ("Usage: netcatrev1.py -t target_host -l -p port")
        print ("netcatrev1.py -l -p port    - listen on port for incoming connections")
        print ("netcatrev1.py -t TargetIP -p port    - connect to target IP and port")
        print("Examples: ")
        print("netcatrev1.py -l -p 1234")
        print("netcatrev1.py -t 192.168.0.1 -p 5555")

        sys.exit(0)


def server(Port):
       
    try:
        # if no target is defined we listen on all interfaces
        TargetIP = "0.0.0.0"
        MyCommand = ""
        BUFFER=1024
        
        MyServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        MyServer.bind((TargetIP,int(Port)))
        MyServer.listen()
        Connection,ClientAddress = MyServer.accept()
        print('Connected by', ClientAddress)
        while True:
            # get c e or f
            Data = Connection.recv(BUFFER)
            DataInStringForm = Data.decode()
            print("Received data ", DataInStringForm)
            if DataInStringForm == "":
                    print("Good bye!!\n")
                    Connection.close()
                    sys.exit(0)
            # get command, executable or file name
            CommandOrFile = Connection.recv(BUFFER)
            print("Received command, executable or file name ", CommandOrFile.decode()) 
            if (DataInStringForm == "c" or DataInStringForm == "e"):
                    if CommandOrFile:
                            MyCommand = run_command(CommandOrFile)
                            if MyCommand:
                                    Connection.send(MyCommand)
                            else:
                                    Connection.send(DataInStringForm.encode())
            elif (DataInStringForm == "f"):
                    try:
                            FileHandle = open(CommandOrFile, "wb")
                            buffer = Connection.recv(BUFFER)
                            while True:
                                    FileHandle.write(buffer)
                                    buffer = Connection.recv(BUFFER)
                                    if not buffer:
                                            print("finished buffering file contents\n")
                                            break
                            FileHandle.close()
                            Connection.close()
                            print("Successfully uploaded file ", CommandOrFile.decode())
                    except:
                            print("Failed to upload file ", CommandOrFile.decode())
            else:       
                  print("Good bye!\n")
                  Connection.close()
                  break
            Connection,ClientAddress = MyServer.accept()
            print('Connected by', ClientAddress)
    finally:
        Connection.close()

def client(TargetIP, Port):

        try:
                BUFFER=1024
                MyInput = input("Pls input the letter c(ommand), f(ile), e(xecutable) or CRLF to exit ")
                while (MyInput != ""):
                        MyClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        MyClient.connect((TargetIP, int(Port)))
                        MyClient.sendall(MyInput.encode())
                        while True:
                                if (MyInput == "c" or MyInput == "e"):
                                        MyInput = input("Pls input the command or executable file ")
                                        MyClient.sendall(MyInput.encode())       
                                        Data = MyClient.recv(BUFFER)
                                        print('Received', Data.decode())
                                        break
                                elif (MyInput == "f"):
                                        FileName = input("Pls input the file name to be uploaded ")
                                        try:
                                                MyClient.sendall(FileName.encode())       
                                                FileHandle = open(FileName, "rb")
                                                FileContents = FileHandle.read(BUFFER)
                                                while (FileContents):
                                                        MyClient.send(FileContents)
                                                        FileContents = FileHandle.read(BUFFER)
                                                FileHandle.close()
                                                print("Successfully sent contents of file ", FileName)
                                                break
                                        except:
                                                print("Could not open and send contents to ", FileName)
                                                break
                                else:
                                        print("No c e or f inputted. Shutting down. ")
                                        MyClient.close()
                                        sys.exit(0)
                        MyInput = input("Pls input the letter c(ommand), f(ile), e(xecutable) or CRLF to exit ")
                        MyClient.sendall(MyInput.encode())
        except:
                print("Something went wrong in the Client function ")
                sys.exit(0)
        finally:
                MyClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                MyClient.connect((TargetIP, int(Port)))
                MyClient.sendall(MyInput.encode())
                print("Closing Client. Good bye!!\n")
                MyClient.close()

# this runs a command and returns the output
def run_command(command):
        
        # trim the newline
        command = command.rstrip()
        # run the command and get the output back
        try:
#                print("The command is ", command)
                output = subprocess.check_output(command.decode(),stderr=subprocess.STDOUT, shell=True)
        except:
                output = "Failed to execute command.\r\n"
        
        # send the output back to the client
        return output


def main(argv):
        if not len(sys.argv[1:]):
            usage()

        if (len(sys.argv) == 5):
                client(sys.argv[2], sys.argv[4])
        elif (len(sys.argv) == 4):
                server(sys.argv[3])
        elif (len(sys.argv) == 7):
                client(sys.argv[2], sys.argv[4], sys.argv[6])

        else:
                usage()



main(sys.argv[1:])
    
              
              
