import datetime
import threading
from socket import *

# text coloring codes
OKGREEN = '\033[92m'
ENDC = '\033[0m'
FAIL = '\033[91m'

# math operations string format
operations = ['*', '/', '^', '-', '+']


# check if a string can be parsed to float
def isfloat(string):
    try:
        float(string)
        return True

    except ValueError:
        return False


# two methods below is for logging
def reqReceiverLogger(address, text):
    print(OKGREEN + 'Request received from IP: ' + address[0] + ' Port:' + str(address[1])
          + ' at: ' + str(datetime.datetime.now()) + ' request text: ' + '"' + text + '"' + ENDC)


def messageSenderLogger(address, text):
    print(OKGREEN + 'Message sent to IP: ' + address[0] + ' Port:' + str(address[1])
          + ' at: ' + str(datetime.datetime.now()) + ' message text: ' + '"' + text + '"' + ENDC)


def serviceToClient(TCPConnection, clientAddress):
    while True:
        try:
            greeting = TCPConnection.recv(2048).decode()
            reqReceiverLogger(clientAddress, greeting)

            # check if client job is done or not
            if greeting == 'exit':
                message = 'connection closed'
                TCPConnection.send(message.encode())
                messageSenderLogger(clientAddress, message)

                TCPConnection.close()
                print(OKGREEN + 'Connection with client with IP: ' + clientAddress[0] + ' Port:' + str(clientAddress[1])
                      + ' at: ' + str(datetime.datetime.now()) + ' closed' + ENDC)
                break

            # check if the clients starts the job or not
            if greeting != 'start':
                message = 'not a valid input(enter start/exit)'
                TCPConnection.send(message.encode())
                messageSenderLogger(clientAddress, message)

                continue

            # sending ack to client
            TCPConnection.send('OK'.encode())
            messageSenderLogger(clientAddress, 'Ok')

            # getting a number from client
            firstNumber = TCPConnection.recv(2048).decode()
            reqReceiverLogger(clientAddress, firstNumber)

            # check if client's input is valid or not
            if firstNumber == 'exit':
                message = 'connection closed'
                TCPConnection.send(message.encode())
                messageSenderLogger(clientAddress, message)

                TCPConnection.close()
                print(OKGREEN + 'Connection with client with IP: ' + clientAddress[0] + ' Port:' + str(clientAddress[1])
                      + ' at: ' + str(datetime.datetime.now()) + ' closed' + ENDC)
                break

            if not isfloat(firstNumber):
                message = 'not a valid number'
                TCPConnection.send(message.encode())
                messageSenderLogger(clientAddress, message)

                continue

            TCPConnection.send('OK'.encode())
            messageSenderLogger(clientAddress, 'Ok')

            secondNumber = TCPConnection.recv(2048).decode()
            reqReceiverLogger(clientAddress, secondNumber)

            if secondNumber == 'exit':
                message = 'connection closed'
                TCPConnection.send(message.encode())
                messageSenderLogger(clientAddress, message)

                TCPConnection.close()
                print(OKGREEN + 'Connection with client with IP: ' + clientAddress[0] + ' Port:' + str(clientAddress[1])
                      + ' at: ' + str(datetime.datetime.now()) + ' closed' + ENDC)
                break

            if not isfloat(secondNumber):
                message = 'not a valid number'
                TCPConnection.send(message.encode())
                messageSenderLogger(clientAddress, message)

                continue

            TCPConnection.send('OK'.encode())
            messageSenderLogger(clientAddress, 'OK')

            operation = TCPConnection.recv(2048).decode()
            reqReceiverLogger(clientAddress, operation)

            if operation == 'exit':
                message = 'connection closed'
                TCPConnection.send(message.encode())
                messageSenderLogger(clientAddress, message)

                TCPConnection.close()
                print(OKGREEN + 'Connection with client with IP: ' + clientAddress[0] + ' Port:' + str(clientAddress[1])
                      + ' at: ' + str(datetime.datetime.now()) + ' closed' + ENDC)
                break

            # check if operation that client asked for is valid or not
            if operation not in operations:
                message = 'not a valid operation signature'
                TCPConnection.send(message.encode())
                messageSenderLogger(clientAddress, message)

                continue

            # this is for don't let server fail if a mathematical calculation result was not valid
            try:
                result = 0.0

                # different types of operations
                if operation == '+':
                    result = float(firstNumber) + float(secondNumber)

                if operation == '-':
                    result = float(firstNumber) - float(secondNumber)

                if operation == '*':
                    result = float(firstNumber) * float(secondNumber)

                if operation == '/':
                    result = float(firstNumber) / float(secondNumber)

                if operation == '^':
                    result = float(firstNumber) ** float(secondNumber)

                TCPConnection.send(str(result).encode())
                messageSenderLogger(clientAddress, str(result))

            # if result of operation was not valid
            except:
                message = 'result of operation was not a number(NaN)'
                TCPConnection.send(message.encode())
                messageSenderLogger(clientAddress, message)

        # if suddenly client disconnected we use this to don't let server fails
        except:
            print(FAIL + 'Client with IP: ' + clientAddress[0] + ' Port:' + str(clientAddress[1])
                  + ' at: ' + str(datetime.datetime.now()) + ' disconnected' + ENDC)
            break


# main

# process port in server
thisServerPort = 33333

# making a TCP socket
serverTCPSocket = socket(AF_INET, SOCK_STREAM)

# this server socket only answers to one client at same time
serverTCPSocket.bind(('', thisServerPort))

# can listen to 100 clients at same time
serverTCPSocket.listen(100)

print('Server is on and ready: ')

# main server loop
while True:
    # opening connection with a client
    TCPConnection, clientAddress = serverTCPSocket.accept()
    # connection log
    print(OKGREEN + 'Client with IP: ' + clientAddress[0] + ' Port:' + str(clientAddress[1])
          + ' at: ' + str(datetime.datetime.now()) + ' connected' + ENDC)
    x = threading.Thread(target=serviceToClient, args=(TCPConnection, clientAddress))
    x.start()
