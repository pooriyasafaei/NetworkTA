import datetime
from socket import *

# text coloring codes
OKGREEN = '\033[92m'
ENDC = '\033[0m'
FAIL = '\033[91m'


# two methods below is for logging
def messageReceiverLogger(address, message):
    print(OKGREEN + 'Message received from IP: ' + address[0] + ' Port: ' + str(address[1])
          + ' at: ' + str(datetime.datetime.now()) + ' message text: ' + '"' + message + '"' + ENDC)
    print('\nMessage from server: ' + message + '\n')


def reqSenderLogger(address, message):
    print(OKGREEN + 'Request sent to IP: ' + address[0] + ' Port: ' + str(address[1])
          + ' at: ' + str(datetime.datetime.now()) + ' request text: ' + '"' + message + '"' + ENDC)


# port and IP of server
destServerAddress = ('127.0.0.1', 33333)

# making a TCP socket
TCPSocket = socket(AF_INET, SOCK_STREAM)

try:
    # making a TCP connection with server
    TCPSocket.connect(destServerAddress)
    print(OKGREEN + 'Connected to server with IP: ' + destServerAddress[0] + ' Port:' + str(destServerAddress[1])
          + ' at: ' + str(datetime.datetime.now()) + ENDC)

    # is for the time that server is not reachable
    try:

        while True:
            # first req to server
            greeting = input('Enter "start" to notify server: ')
            TCPSocket.send(greeting.encode())
            reqSenderLogger(destServerAddress, greeting)

            response = TCPSocket.recv(2048)
            messageReceiverLogger(destServerAddress, response.decode())

            # check if server closed the connection or not
            if response.decode() == 'connection closed':
                TCPSocket.close()
                print(OKGREEN + 'Connection with server with IP: ' + destServerAddress[0] + ' Port:' + str(
                    destServerAddress[1])
                      + ' at: ' + str(datetime.datetime.now()) + ' closed' + ENDC)
                break
            # check if that server accepted req or not
            if response.decode() != 'OK':
                continue

            # sec req to server
            Number = input('Enter first number: ')
            TCPSocket.send(Number.encode())
            reqSenderLogger(destServerAddress, Number)

            response = TCPSocket.recv(2048)
            messageReceiverLogger(destServerAddress, response.decode())

            if response.decode() == 'connection closed':
                TCPSocket.close()
                print(OKGREEN + 'Connection with server with IP: ' + destServerAddress[0] + ' Port:' + str(
                    destServerAddress[1])
                      + ' at: ' + str(datetime.datetime.now()) + ' closed' + ENDC)
                break
            if response.decode() != 'OK':
                continue

            Number = input('Enter second number: ')
            TCPSocket.send(Number.encode())
            reqSenderLogger(destServerAddress, Number)

            response = TCPSocket.recv(2048)
            messageReceiverLogger(destServerAddress, response.decode())

            if response.decode() == 'connection closed':
                TCPSocket.close()
                print(OKGREEN + 'Connection with server with IP: ' + destServerAddress[0] + ' Port:' + str(
                    destServerAddress[1])
                      + ' at: ' + str(datetime.datetime.now()) + ' closed' + ENDC)
                break
            if response.decode() != 'OK':
                continue

            operation = input('Enter operation: ')
            TCPSocket.send(operation.encode())
            reqSenderLogger(destServerAddress, operation)

            response = TCPSocket.recv(2048)
            messageReceiverLogger(destServerAddress, response.decode())

            if response.decode() == 'connection closed':
                TCPSocket.close()
                print(OKGREEN + 'Connection with server with IP: ' + destServerAddress[0] + ' Port:' + str(
                    destServerAddress[1])
                      + ' at: ' + str(datetime.datetime.now()) + ' closed' + ENDC)
                break

            print('final result from server: ' + response.decode() + '\n\n')

    # if connection suddenly closed
    except:
        print(FAIL + '\nConnection to server with IP: ' + destServerAddress[0] + ' Port:' + str(
            destServerAddress[1])
              + ' at: ' + str(datetime.datetime.now()) + ' failed' + ENDC)

# if connection could not be established
except:
    print(FAIL + '\nCouldnt establish connection to server with IP: ' + destServerAddress[0] + ' Port:' + str(
        destServerAddress[1])
          + ' at: ' + str(datetime.datetime.now()) + ENDC)
