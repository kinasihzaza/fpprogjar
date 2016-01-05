import select
import os
import socket
import sys
import signal
import threading
import time
import platform
import datetime
import os.path
import urllib2 #Transform URL string into normal string in python (%20 to space etc)

ip = 'localhost'

f1 = open("httpserver.conf","r")
portConf = int(f1.read())

f2 = open("./error.html","r")
errorRespond = f2.read()

f3 = str("./saddam.html")
#tigaratusRespond = f3.read()

f4 = str("./dhea.html")

f5 = str("./ucup.html")

#local variabel
os1 = platform.system()
os2 = platform.release()
ver = sys.version
tgl = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

class Server:
    def shutdown(self):
     try:
         print("Shutting down the server")
         s.socket.shutdown(socket.SHUT_RDWR)
     except Exception as e:
         print("Warning: could not shut down the socket. Maybe it was already closed?",e)
    def keyboardKill(sig, dummy):
        """ Shutdown By SIGINT """
        s.shutdown()
        sys.exit(1)
    def __init__(self):
        self.host = 'localhost'
        self.port = portConf
        self.backlog = 5
        self.size = 4096
        self.server = None
        self.threads = []

    def open_socket(self):        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host,self.port))
        self.server.listen(100)
        
    def run(self):
        self.open_socket()
        input = [self.server, sys.stdin]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:

                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

        # close all threads

        self.server.close()
        for c in self.threads:
            c.join()
    signal.signal(signal.SIGINT, keyboardKill)


class Client(threading.Thread):

    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 4096

    def run(self):
        running = 1
        data = self.client.recv(self.size)
        print "Requested : "+data
        tempo = data.split()
        #print tempo
        print "METHOD : "+ tempo[0]
        method = tempo[0]
        namaFile = tempo[1]
        namaFile = namaFile[1:]
        #print namaFile
        namaFile=urllib2.unquote(namaFile)
        #IF METHOD GET
        if(method == "GET"):
            if os.path.isfile(namaFile):
                print "FILENYA ADALAH : "+ str(namaFile)
                if(namaFile.rfind('.php')>=0) or (namaFile.rfind('.html')>=0):
                    if(namaFile.rfind('.php')>=0):
                        
                        commandPHP="php -f " + namaFile+" >temp.html"
                        os.system(commandPHP) 
                        dataTemp=open("temp.html","r")
                        os.system('rm -rf temp.html')

                    else:
                        if(namaFile == "saddam.html"):
                            dataTemp = open(f3,"r")
                        else:
                            dataTemp = open(namaFile,"r")

                    if(namaFile == "saddam.html"):
                        self.client.send("HTTP/1.1 301 Moved Permanently\nContent-Type: text/html\nContent-Language: id\r\n\r\n")
                    
                    elif (namaFile == "dhea.html"):
                        self.client.send("HTTP/1.1 403 Forbidden\nContent-Type: text/html\nContent-Language: id\r\n\r\n")

                    elif (namaFile == "ucup.html"):
                        self.client.send("HTTP/1.1 500 Internal Server Error\nContent-Type: text/html\nContent-Language: id\r\n\r\n")

                    else:    
                        self.client.send("HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Language: id\r\n\r\n")

                    while 1:
                        dataR = dataTemp.read(4096)
                        #print dataR
                        self.client.send(dataR)
                        if dataR == "":
                            break
                else:
                    self.client.send('HTTP/1.1 200 OK\nAccept-Ranges: bytes\nConnection: Keep-Alive\nContent-Type: application/x-gzip\nContent-Language: id\r\n\r\n')
                    data=""
                    files = open(namaFile,"r")
                    while 1: 
                        dataTemp = files.read(4096)
                        self.client.send(dataTemp)
                        if dataTemp=="":
                            break
            elif os.path.isdir(namaFile) or namaFile == "":
                self.client.send("HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Language: id\r\n\r\n")
                if namaFile == "":
                    namaFile = "."
                dataTemp = os.listdir(namaFile)
                line= "---------------------------------"
                print line
                print "List Dir :"
                print line
                number = 0
                number2=len(dataTemp)
                for ahay in dataTemp:
                    if (number==number2):
                        continue
                    print ">> "+dataTemp[number]
                    number = number +1

                if "index.html" in dataTemp or "index.php" in dataTemp:
                    if "index.html" in dataTemp:
                        dataTemp = open("./home/index.html","r")
                    else:
                        tempE  = "php -f index.php > temp.html"
                        os.system(tempE)
                        dataTemp = open("temp.html","r")
                        os.system("rm -rf temp.html")
                    while 1:
                        dataR = dataTemp.read(4096)
                        #print dataR
                        self.client.send(dataR)
                        if dataR=="":
                            break
                else: #list Dir
                    index=len(dataTemp)
                    namafolder = namaFile.split("/")
                    print namafolder
                    namafolder[0]
                    head = '''
                        <html>
                        <head>
                        <title>Index of /%s...</title>
                        </head>
                        <body>
                        <h1>Index of /%s...</h1>
                        <table>
                        <tr>
                        <td><a href="/%s"><font color = "green">Parent Directory</font></a></td>
                        <tr><th colspan="200"><hr></th></tr>
                        <tr><td valign="top"></td>
                        </tr>
                        <tr>
                        <td><p><strong>Name<strong></p></td>
                        <td><p><strong>Size(Byte)<strong></p></td>
                        <td><p><strong>&emsp;Last Modified<strong></p></td>
                        </tr>
                        <tr><th colspan="200"><hr></th></tr>
                        <tr><td valign="top"></td>
                        
                        '''%(namaFile,namaFile,namafolder[0])
                    base = "./"

                    for i in range(0,index):
                        filePath=base+namaFile+"/"+dataTemp[i]
                        sizeFile=os.path.getsize(filePath)
                        modifiedFile=time.ctime(os.path.getmtime(filePath))
                        
                        if(sizeFile==4096):
                            sizeFile = "~"
                        body = '''
                        <tr>
                        <td><a href='/%s/%s'>%s</a></td>
                        <td>%s</td>
                        <td>&emsp;%s</td>
                        </tr>
                        '''%(namaFile,dataTemp[i],dataTemp[i],sizeFile,modifiedFile)
                        head = head +body
                    tail = '''
                    </table>
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    <address> ZazaSaddamDhitaDhea Server Running On (%s / %s) </adress>
                    '''%(ip, portConf)
                    
                    self.client.send(head)
                    self.client.send(tail)
            else:
                print "File Requested : "+namaFile+" not Found on server"
                sizeleng = os.path.getsize('saddam.html')
                x = "HTTP/1.1 404 Not Found\nAccept-Ranges: bytes\nConnection: Keep-Alive\nContent-Type: application/x-gzip\nContent-Type: text/html\nServer: Python "+str (ver)+str (os2)+str (os1)+"\nContent-Length: "+str(sizeleng)+"\nDate: "+str(tgl)+"\nContent-Language: id \n \r\n\r\n"
                y = errorRespond
                z = str(x)+str(y)
                self.client.send(z)
                dataTemp = errorRespond
        #IF METHOD POST
        elif(method == "POST"):
            self.client.send('HTTP/1.1 200 OK\nAccept-Ranges: bytes\nConnection: Keep-Alive\nContent-Type: application/x-gzip\nContent-Language: id\r\n\r\n')
   #        print "inidata" +data
            
            m = data.split ("\r\n\r\n")
            requestHeaderPostMethod = m[0]
            postValue = m[1]
            print "ini post value : " +postValue
            s = postValue.split ("&")
            var1 = s[0]
            var2 = s[1]
            var1sesungguhnya = var1.split ("=")
            var1sesungguhnya = var1sesungguhnya[1]
            var2sesungguhnya = var2.split ("=")
            var2sesungguhnya = var2sesungguhnya[1]
            hasilJumlah = str (var1sesungguhnya) + str (var2sesungguhnya)
            print "hasil post " +str (hasilJumlah)
            x = namaFile
            #if(namaFile.split(""))
#            print "ini x" +x
            files = open(x,"r")
 #           print "xoxo"
            data=""
            self.client.send (str (hasilJumlah)+"\n")
       #     while 1: 
   #             dataTemp = files.read(4096)
  #              print dataTemp
    #            self.client.send(hasilJumlah)
     #           if dataTemp=="":
      #              break  
        elif(method == "HEAD"):   
            self.client.send("HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Language: id\r\n\r\n")
            print "FILENYA ADALAH : "+ str(namaFile)
            dataTemp = open(namaFile, 'r')
            while 1:
                dataR = dataTemp.read(4096)
                #print dataR
                self.client.send(dataR)
                if dataR == "":
                    break
        self.client.close();


if __name__ == "__main__":
    s = Server()
    s.run() 
