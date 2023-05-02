import time
from socket import *

ip = '127.0.0.1'
server_port = 1010
# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
clientSocket = socket(AF_INET, SOCK_DGRAM)

# To set waiting time of one second for reponse from server
clientSocket.settimeout(5)

# Declare server's socket address
remoteAddr = (ip, server_port)

# Ping ten times
for i in range(10):

    sendTime = time.time()
    message = 'ping ' + str(i + 1) + " " + str(time.strftime("%H:%M:%S"))
    clientSocket.sendto(message.encode(), remoteAddr)

    try:
        data, server = clientSocket.recvfrom(1024)
        recdTime = time.time()
        rtt = recdTime - sendTime
        print("Message Received", data.decode())
        print("Round Trip Time", rtt)

    except timeout:
        print('REQUEST TIMED OUT')
