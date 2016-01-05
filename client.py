import socket
import os

f1 = open('webPage1.txt', 'w')
#f2 = open('webPage2.txt', 'w')
fH = open('hasil.txt', 'w')

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('127.0.0.1', 8080)
# client_socket.connect(server_address)


response = ''
loading=1
try:
        while 1:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_address = ('127.0.0.1', 8080)
                client_socket.connect(server_address)    
                file_request = raw_input()
                method = file_request.split(" ")
                method = method[0]

                if file_request.split(" ")[0] == "GET" or file_request.split(" ")[0]=="HEAD":
                        request_header =  file_request.split(" ")[0]+' /'+file_request.split(" ")[1]+' HTTP/1.1\r\nHost: http://localhost\r\n\r\n'
                        #print request_header
                        client_socket.send(request_header)
                        response = ""
                        while 1:
                                recv = client_socket.recv(1024)
                                if not recv:
                                        break

                                response +=  recv    
                        
                        if (method == "HEAD"):
                                xy = response.split ("\r\n\r\n")
                                xy = xy[1]
                                client_socket.close()
                        else:
                                xy = response
                        print xy
                        #client_socket.close()

                elif file_request.split(" ")[0] == "POST":
                        if(file_request.split(" ")[1].rfind('.php')>=0):
                                commandPHP="php -f " + file_request.split(" ")[1]+" >temp.html"
                                os.system(commandPHP) 
                                dataTemp=open("temp.html","r")
                                os.system('rm -rf temp.html')
                        client_socket.close()

                a = open("hasil.html","w")
                a.write(response)
                a.close()
                client_socket.close()
        f1.write(response)
        #---------------------------------------------#

        #f1.close()
        #f2.close()
        #fH.close()

except KeyboardInterrupt:
        f1.close()
        #f2.close()
        fH.close()
        client_socket.close()
        sys.exit(0)